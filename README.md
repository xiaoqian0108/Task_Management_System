# Task Management System
## 紀錄
- 0329: http://127.0.0.1:8000/tasks/

-0415 by Siowan
    1. DB建立 由於Event需要DataBase存放數據，所以我用MySQL新增了一個DataBase，並且把db.sqlite3(Django內建的DB)的內容遷移到Django_SQL.sql
        [SQL 使用MySQL 8.3.0]
        - <__init__.py>
            import pymysql
            pymysql.install_as_MySQLdb()
            -> 將pymysql視為MySQLdb，使Django能夠正確地與MySQL數據庫進行交互。
                原因：Django中使用MySQL數據庫時，Django的某些部分預期導入的是MySQLdb庫，但在Python3 中，MySQLdb 庫不再被廣泛支持。
        - 遷移指令：    
            python manage.py makemigrations (APP_NAME)
            python manage.py migrate
        - <tasksmanagement/setting.py> 修改
            - 在INSTALLED_APPS的list中加入我們APP（tasks）-> 告訴 Django在專案中包含這個應用程式，Django就會相應地加載和管理它。
            
            - 在開頭import os，以便進行下面操作
            
            - TEMPLATE的 'DIRS': [os.path.join(BASE_DIR, 'templates')] -> 要渲染的HTML都放在'templates'目錄中，os.path.join(BASE_DIR, 'templates') 將構建出templates目錄的完整路徑
    
    2. tasks目錄下的修改
        - <tasks/urls.py>
            - 根據新增的功能對應配置子路由
        - <tasks/models.py>
            - 在models.py中創建了一個新的模型用來存放Event的資訊
            - Event继承自models.Model
            - Data：
                id是識別Event名稱的主鍵，Event的主鍵是唯一的
                name是Event名稱，每個Event的name可以重複
                label是Event的標籤，用於對Event進行分類
                date是Event的日期
            - Method：
                def __str__(self)
                -> 當我們在shell中輸入Event.objects.all()時，我們希望返回事件
        - <tasks/template>
            - 新建了template的文件夾用來存放渲染的html
            - 首頁，包含了創建及查詢Event、以及跳轉到其他頁面的按鈕：create_event.html
                可以通過輸入名稱（Name）、標籤（Label）、日期（Date）進行創建Event
                可以在查詢欄輸入查詢之Event的標籤（Label）找到對應的Event
            - 分類表頁面： categorized_events.html
                根據標籤（Label）進行分類並顯示在頁面
            - 進行删除Event的頁面： delete_event.html
                可以點擊checkbox選擇Event，按下按鈕即可删除（可多選）
            - 進行Event內容修改的頁面： update_event.html
                可以點擊checkbox選擇Event，在對應想修改內容的輸入框填寫新資訊，按下按鈕即可（僅單選），這裏只要輸入至少一個輸入框也可以修改對應資訊，若三個輸入框皆無填寫則網頁回應會顯示失敗訊息
        - <tasks/views.py>
            - 創建一個Class名為EventManager -> 實作所有和Event管理相關的動作
            Method：
                1. tocreate_event(request): 跳轉到/tasks
                2. create_event(request): 
                    目的：新增Event的Object並存到資料庫中
                    利用POST拿到首頁填寫創建Event的三項Data並賦值給name, label, date
                    進行邏輯判斷看三個Data是否都不為空
                    如果都不為空則把新創一個object到Event Class內，並且返回成功訊息
                    如果變數皆為空，則返回失敗的訊息。
                3. toupdate_event(request): 跳轉到/tasks/update_event
                4. update_event(request):
                    目的：負責接收用戶提交的事件更新數據，將更新應用到數據庫中的相應事件，並返回相應的成功或失敗訊息給用戶
                    實作方法：
                    利用POST拿到更新Event頁面填寫創建Event的三項Data並賦值給name, label, date，並且還獲取事件的 ID
                    進行邏輯判斷看三個Data是否都不為空
                    如果至少一個不為空則通過事件的ID從數據庫中獲取相應的事件對象，
                    這裏使用get_object_or_404函數從資料庫中查詢指定ID的事件，如果找不到對應的事件，則返回 404 錯誤頁面，若找到則更新對應的Data並返回成功訊息
                    如果變數皆為空，則返回失敗的訊息
                5. todelete_event(request): 跳轉到/tasks/delete_event
                6. delete_event(request): 
                    目的：實現了根據用戶提交的事件 ID，刪除數據庫中對應的事件的功能
                    實作方法：
                    利用POST拿到删除頁面中checkbox被選擇的events的id列表
                    遍歷這些Events的id，並根據每個id使用Event.objects.filter(id=event_id).delete()來從資料庫中刪除相應的事件
                    刪除操作完成後返回成功訊息
                    如果請求的方法不是POST，則直接返回，不執行任何操作
                7. categorized_events(request):
                    目的：按標籤（Label）分類事件並在網頁上顯示
                    實作方法：
                    通過Event.objects.values_list('label', flat=True).distinct()從數據庫中獲取所有不重複的標籤(label) 列表
                    創建了一個空字典categorized_events來存儲按標籤分類後的事件
                    之後再遍歷每個不重複的標籤，並將該標籤對應的事件過濾出來，存儲在 categorized_events中
                    分類好的事件傳遞給categorized_events.html，並將其作為 categorized_events的值，以供html使用。
                8. search_events(request):
                    目的：根據標籤(label) 進行事件搜索並在網頁上顯示搜索結果
                    實作方法：
                    利用GET取得在查詢輸入框所填寫的event_label
                    使用Event.objects.filter(label__icontains=search_label)從數據庫中過濾具有包含搜索標籤的事件
                    檢查是否有符合搜索標籤的事件
                    如果有符合，則使用列表推導式將搜索結果中每個事件的名稱、標籤和日期格式化為字符串，並使用<br>標籤連接起來，最後將其作為HTTP響應返回。
                    如果沒有符合搜索標籤的事件，則返回失敗訊息
                    如果請求方法不是GET，則什麼也不做
