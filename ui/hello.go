package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
	"log"
	"net/http"
)

// ScanRecord 用于映射SCAN表中的记录
type ScanRecord struct {
	ID        int    `json:"id"`
	IP        string `json:"ip"`
	Method    string `json:"method"`
	TimeStamp string `json:"timeStamp"`
}

// IPRecord 用于映射ip表中的记录
type IPRecord struct {
	ID         int    `json:"id"`
	IP         string `json:"ip"`
	Method     string `json:"method"`
	DeviceInfo string `json:"deviceInfo"`
	HoneyPot   string `json:"honeyPot"`
	TimeStamp  string `json:"timeStamp"`
}

// ServiceRecord 用于映射Service表中的记录
type ServiceRecord struct {
	ID         int    `json:"id"`
	IP         string `json:"ip"`
	Method     string `json:"method"`
	Port       int    `json:"port"`
	Protocol   string `json:"protocol"`
	ServiceApp string `json:"serviceApp"`
	TimeStamp  string `json:"timeStamp"`
}

func main() {

	// 设置静态文件的目录
	fs := http.FileServer(http.Dir("./static"))

	// 将根路由`/`映射到静态文件服务器，使用http.StripPrefix来移除URL路径中的前缀
	// 这样，当访问http://localhost:8080/cover.html时，就会返回./static/cover.html文件
	http.Handle("/", http.StripPrefix("/", fs))

	http.HandleFunc("/scans", handleScans)
	http.HandleFunc("/ips", handleIPs)
	http.HandleFunc("/services", handleServices)

	fmt.Println("Server is running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func handleScans(w http.ResponseWriter, r *http.Request) {
	scans, err := getScans()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(scans)
}

func handleIPs(w http.ResponseWriter, r *http.Request) {
	ip := r.URL.Query().Get("ips")
	ips, err := getIPs(ip)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(ips)
}

func handleServices(w http.ResponseWriter, r *http.Request) {
	ip := r.URL.Query().Get("ip")
	services, err := getServices(ip)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(services)
}

// getScans, getIPs, 和 getServices 函数的实现...
// 这里需要实现从数据库查询数据的逻辑，类似于之前的getScans函数。
// 注意：getIPs和getServices函数应该根据传入的ip参数动态构建SQL查询。

// getScans 从数据库查询SCAN表，并返回查询结果
func getScans() ([]ScanRecord, error) {
	db, err := sql.Open("sqlite3", "/home/sqlite.db")
	if err != nil {
		return nil, err
	}
	defer db.Close()

	rows, err := db.Query("SELECT id, ip, Method, TimeStamp FROM SCAN")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var scans []ScanRecord
	for rows.Next() {
		var s ScanRecord
		if err := rows.Scan(&s.ID, &s.IP, &s.Method, &s.TimeStamp); err != nil {
			fmt.Println("fuck!")
			return nil, err
		}
		scans = append(scans, s)
	}

	if err = rows.Err(); err != nil {
		return nil, err
	}

	return scans, nil
}

func getIPs(ip string) ([]IPRecord, error) {
	db, err := sql.Open("sqlite3", "/home/sqlite.db")
	if err != nil {
		return nil, err
	}
	defer db.Close()

	rows, err := db.Query("SELECT id, ip, Method, DeviceInfo, HoneyPot, TimeStamp FROM IP")

	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var iprecord []IPRecord
	for rows.Next() {
		var s IPRecord
		if err := rows.Scan(&s.ID, &s.IP, &s.Method, &s.DeviceInfo, &s.HoneyPot, &s.TimeStamp); err != nil {
			return nil, err
		}
		iprecord = append(iprecord, s)
	}

	if err = rows.Err(); err != nil {
		return nil, err
	}

	return iprecord, nil
}

func getServices(ip string) ([]ServiceRecord, error) {
	db, err := sql.Open("sqlite3", "/home/sqlite.db")
	if err != nil {
		return nil, err
	}
	defer db.Close()

	var rows *sql.Rows
	//rows, err := db.Query("SELECT id, ip, Method, Port, Protocol, Service_App, TimeStamp FROM SERVICES")
	if ip == "" {
		// 当没有提供ip参数时，查询所有TimeStamp不为NULL的记录
		rows, err = db.Query("SELECT id, ip, Method, Port, Protocol, Service_App, TimeStamp FROM SERVICES WHERE TimeStamp IS NOT NULL")
	} else {
		// 当提供了ip参数时，查询对应ip且TimeStamp不为NULL的记录
		rows, err = db.Query("SELECT id, ip, Method, Port, Protocol, Service_App, TimeStamp FROM SERVICES WHERE ip = ? AND TimeStamp IS NOT NULL", ip)
	}
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var servicerecord []ServiceRecord
	for rows.Next() {
		var s ServiceRecord
		if err := rows.Scan(&s.ID, &s.IP, &s.Method, &s.Port, &s.Protocol, &s.ServiceApp, &s.TimeStamp); err != nil {
			return nil, err
		}
		servicerecord = append(servicerecord, s)
	}

	if err = rows.Err(); err != nil {
		return nil, err
	}

	return servicerecord, nil
}
