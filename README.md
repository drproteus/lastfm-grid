<img width="530" alt="image" src="https://github.com/user-attachments/assets/289179dc-a14f-4c39-8479-ded9a452cc75">

# Setup
* `pip install -r requirements.txt`
* `export API_KEY=$LASTFM_API_KEY` (https://www.last.fm/api)
* `flask --app server run`
* `curl -X POST http://localhost:5000/covers/3/3/$USER/overall > ~/covers.jpg`
