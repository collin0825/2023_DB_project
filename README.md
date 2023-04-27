# 中山求職網

我們要設計一個學校工讀媒合系統，該系統需記載職缺的詳細資訊以及應徵者資訊，因此有兩個使用角色分別是學生和處室教職員。

Video Link : https://youtu.be/TsTaL7N71MM

## ERD
<img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/ERD.png' width='600px'>

## Relation Schema
<img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/relation%20schema.jpg' width='600px'>

## 網站畫面
### 學生
- 職缺總覽(首頁)

  <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/user%20vacancy.jpg' width='800px'>
  
- 職缺詳細內容&應徵

  <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/user%20apply.jpg' width='800px'>
  
- 我感興趣清單

  <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/user%20interest.jpg' width='800px'>
  
- 求職紀錄

  <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/user%20record.jpg' width='800px'>
  
  - 查看詳細應徵紀錄
  
    <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/user%20record%20detail.jpg' width='800px'>
    
### 處室教職員
- 職缺管理

 <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/manager%20vacancy.jpg' width='800px'>
 
  - 新增職缺
  
   <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/manager%20add%20vacancy.jpg' width='800px'>

  - 編輯職缺
  
   <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/manager%20edit%20vacancy.jpg' width='800px'>

- 應徵者管理

  <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/manager%20application.jpg' width='800px'>

  - 查看詳細應徵紀錄
  
    <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/manager%20application%20detail.jpg' width='800px'>


- 資料分析
  - 每月應徵數量分析

    <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/manager%20data%20analysis.jpg' width='800px'>
  
  - 各處室歷年職缺數量分析
  
    <img src='https://github.com/collin0825/2023_DB_project/blob/master/readmeImage/manager%20data%20analysis%202.jpg' width='800px'>



### 檔名頁面對照表
#### 中山求職網後台管理網站
檔名 | 對照頁面 |
--- | --- |
productManager | 職缺管理 |
orderManager | 應徵者管理 |
infoManager | 資料維護 |
dashboard | 資料分析 |

#### 中山求職網
檔名 | 對照頁面 |
--- | --- |
productManager | 職缺管理 |
orderManager | 應徵者管理 |
infoManager | 資料維護 |
dashboard | 資料分析 |
