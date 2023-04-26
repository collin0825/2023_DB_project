# 中山求職網

Video Link : https://youtu.be/TsTaL7N71MM

## 需求分析
我們要設計一個學校工讀媒合系統，該系統需記載職缺的詳細資訊以及應徵者資訊，因此有兩個使用角色分別是學生和處室教職員。其資料需求如下：
- **會員(Member)**： 包括會員編號(mId)、姓名(name)、身分證(pId)、生日(birth)、電話(phone)、性別(gender)、系所(dept)、年級(grade)、電子郵件(email)、密碼(password)以及系統身分別(identity)，其中會員編號是唯一。
- **應徵資訊(Application)**：包括應徵編號(aId)、可工作時段(availableTime)、加分備註(bonus)，應徵編號是唯一。應徵資訊必然屬於一個會員。
- **單位(Department)** ：包括單位編號(dId)、處室(office)、組(division)，其中單位編號為唯一值。
- **職缺(Vacancy)**：包括職缺編號(vId)、職缺名稱(vName)、工作內容(contentl)、工作待遇(salary)、需求人數(required)、上班時段(workTime)、職缺狀態(status)、技能要求(skill)，其中職缺編號是唯一。職缺必然屬於一個單位。
- **感興趣職缺(Interest)**：包括加入時間(addTime)，其中沒有任何一個屬性是唯一。感興趣職缺必然屬於一個會員。

此外，Application 跟 Vacancy 間有一個記錄 (Records) 的關係型態，其中記錄了職缺應徵時間(time)、應徵狀態(status)。Interest 跟 Vacancy 間有一個儲存 (Saves) 的關係型態。



## 功能分析

### 學生
- +註冊/登入+
- ++職缺導覽++：可以搜尋/查看職缺，並進行職缺應徵。
- ++我感興趣++：將感興趣的職缺加入儲存清單，且可透過清單直接點選應徵或刪除。
- ++求職紀錄++：可以從此查看歷史應徵紀錄，以及應徵的審核狀態。
- ++個人檔案++：可以新增/編輯個人資訊。



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
