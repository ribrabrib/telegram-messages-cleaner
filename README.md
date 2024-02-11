# Telegram messages cleanup app

Telegram doesn't have any possibility to remove messages reposted from specific 
chats or containing some keywords. We've created this application to automate this 
process.

Bonus: list of restricted chats in Belarus and some popular keywords, which 
may be interpreted by Lukashenko's regime as a reason for repressions.

## Features

* Delete messages by specified keywords (result is based on telegram search api; 
  works just like a search in the app)
  * Keyword or similar in the message text
  * Reposted from the channel with a name similar to a keyword
  * Media/link preview contains similar keyword
* Visualise messages and reposted channels before remove

By default, messages will be deleted from all chat members (if available)!

## How to use

**Your data safety is on your own risk!**

*All scripts below are written for Windows (other users can usually adopt it by themselves)*

1. Register Telegram app: [form](https://my.telegram.org/auth?to=apps).
   Fill a form, `Url` can be left empty. Copy `api_id` and `api_hash`.
1. Download this repo (`Code` -> `Download ZIP` -> Unarchive it)
1. Fill `api_id` and `api_hash` into main.py
1. Fill in `keywords.csv` with the keywords you want to use for a deletion (comma-separated)
1. Install [python3.9+](https://www.python.org/downloads/release/python-399/)
1. Open Powershell(`win+R` -> type `powershell` -> press Enter) and run
```shell
  python -m venv .venv
  .venv\Scripts\Activate.ps1 # `.venv/bin/activate` for UNIX
  pip install -r requirements.txt
  python main.py
```
1. Follow the instruction of the application.
   All **applicable messages will be deleted for you and a recipient if possible**
1. [Safety step] Delete the whole folder manually or ```DEL /F/Q/S *.*```. Make sure your bin is also clean
1. Open your Telegram app -> Settings -> Devices and remove CPython app

## Выкарыстоўванне ў Беларусі

Для ачыскі рэпостаў з "экстрэмісцкіх" каналаў і патэнцыйна небяспечных паведамленняў
на палітычныя тэмы трэба скапіяваць файл `keywords.csv` з папкі `repressions` у корань каталогу
```powershell
cp repressions/keywords.csv keywords.csv
```
Файл можа быць адрэдагаваны на свой погляд (не змяняючы фармату -- адзін радок праз коску),
спіс забароненых рэсурсаў раіцца пераправерыць на наяўнасць аднаўленняў.
Дасылайце аднаўленыя лісты экстрэмісцкіх фарміраванняў на ribrabrib@proton.me для аднаўлення ў рэпазіторыі.  
**Адпіска ад саміх каналаў не выконваецца, выдаляюцца толькі перасланыя паведамленні!**
