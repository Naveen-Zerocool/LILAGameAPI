##### **LILA Backend API**

**Prerequisites**
1. Docker
2. docker-compose

**Available APIs**
1. Auth
   1. Register
   2. Login
2. Game Mode
   1. List game modes
   2. Get popular game mode based on area code
   3. Set user game preference (area code and game mode)
   4. Get active user game preference (area code and game mode)
   5. Inactive active user game preference

**Contains**
1. APIs
2. API docs (With Swagger UI) - View and try out APIs
3. Admin site - View, Search, Filter and Delete Users, Game Modes, Area Codes and User Preferences 

**Admin Site:** http://127.0.0.1:8000/admin/

**Docs:** http://127.0.0.1:8000/docs/

**Postman Collection and Environment**
    
Below files can be found in the repo. We can run each API sequentially and the test script will check for valid status code and it will set the environment variables with necessary data. We can also run it with Postman runner. Have used random generators at register API
1. LILA Backend APIs.postman_collection.json
2. LILA Backend API Environment.postman_environment.json


**System Design Doc** - [link](https://docs.google.com/document/d/1qQXcMhwbndrOqALV9qXwj7I9-fcGNHaZwSlmPrDWKEE/edit?usp=sharing)


**Steps to Run on Local Machine:**

1. git clone <repo_url>
2. docker-compose -f docker-compose.yml up -d --build
3. docker exec -it lilagameapi_lila-backend_1 bash
4. python3 manage.py shell
5. python3 manage.py createsuperuser
6. `for game_mode in ["Capture the Flag", "Team Deathmatch", "Battle Royal"]:
                GameMode.objects.create(name=game_mode)`

Run above snippet on shell to create 3 game modes. Or follow step 7 to add game modes manually
7. Go to http://127.0.0.1:8000/admin and login using the credentials created on step 4, Game Mode will be shown on dashboard. Kindly add  the game modes if adding manually
8. We can use API docs or API postman collection to try out the APIs
9. In Postman first import environment file and then API collection file
