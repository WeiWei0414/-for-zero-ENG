# -for-zero-ENG
將要處理的音檔，跟程式放在同一個資料夾
這是zero english影片格式專用的腳本的code，\n
使用方法有幾點要注意\n
檔名命名須符合規則，\n
女2s、男2s、中文、慢速版、分解版女、分解版男、女4s、男4s\n
另外環境必須建置一些東西，首先到vs code\n
按下ctrl+shift+P，搜尋並選取: Python:Select Interpreter，\n
![image](https://github.com/user-attachments/assets/c5d8af0c-0c46-46cd-887f-8814bc514fa6)
選取全域環境，然後再按windows+R，輸入cmd，進入之後，安裝兩個函式庫
指令:pip install pydub，pip install ffmpeg
然後把ffmpeg-7.1-essentials_build這個資料夾放到安全的地方
接著點進去，進去bin裡面，如圖
![image](https://github.com/user-attachments/assets/9ede5bf0-05d0-499a-b0e0-c2cf8fb535b9)
複製這串路徑，按下windows+S，搜尋系統環境變數
![image](https://github.com/user-attachments/assets/463d7704-c62f-46a6-ace6-b5aa58fb37f2)
點選後，按下環境變數
![image](https://github.com/user-attachments/assets/71ff1fc6-81e7-4b72-822f-1aaa97ed14b7)
上面得框框，選Path，按下編輯，再點選新增，
把剛剛複製的路徑貼上去，按確定，這樣子腳本就能跑了


