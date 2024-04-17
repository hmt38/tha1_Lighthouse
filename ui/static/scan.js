function fetchScanDataAndUpdateTable() {
    fetchScanAndUpdate(); // 立即执行一次更新操作
}
function fetchIPDataAndUpdateTable() {
    fetchIPAndUpdate(); // 立即执行一次更新操作
}
function fetchServicesDataAndUpdateTable() {
    fetchServicesAndUpdate(); // 立即执行一次更新操作
}


function fetchScanAndUpdate() {
    fetch('/scans')
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                updateTableHeader(Object.keys(data[0]));
                updateTableBody(data);
            }
        })
        .catch(error => console.error('Error fetching data: ', error));
}

function fetchIPAndUpdate() {
    fetch('/ips')
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                updateTableHeader(Object.keys(data[0]));
                updateTableBody(data);
            }
        })
        .catch(error => console.error('Error fetching data: ', error));
}
function fetchServicesAndUpdate() {
    fetch('/services')
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                updateTableHeader(Object.keys(data[0]));
                updateTableBody(data);
            }
        })
        .catch(error => console.error('Error fetching data: ', error));
}


function updateTableHeader(keys) {
    const tableHead = document.getElementById('data-table').getElementsByTagName('thead')[0];
    const row = tableHead.insertRow(0); // 创建新的表头行
    tableHead.innerHTML = ''; // 清空当前的表头

    // 为每个键创建一个<th>元素并添加到表头行中
    // keys.forEach(key => {
    //     const tr = document.createElement('tr');
    //     Object.values(key).forEach(text => {
    //         const th = document.createElement('th');
    //         th.textContent = text;
    //         tr.appendChild(th);
    //     });
    //     tableHead.appendChild(tr);
    // });
    const tr = document.createElement('tr');
    keys.forEach(key => {
        const th = document.createElement('th');
        th.textContent = key;
        tr.appendChild(th);
    });
    tableHead.appendChild(tr)
}

function updateTableBody(data) {
    const tableBody = document.getElementById('data-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // 清空当前表格内容

    // 为每个数据对象创建一个表格行
    data.forEach(rowData => {
        const tr = document.createElement('tr');
        Object.values(rowData).forEach(text => {
            const td = document.createElement('td');
            td.textContent = text;
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}
