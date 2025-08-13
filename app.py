from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

ROBLOX_API_USER = "https://users.roblox.com/v1/users/{}"
ROBLOX_API_USERNAME = "https://api.roblox.com/users/get-by-username?username={}"

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    error = None
    if request.method == "POST":
        search_type = request.form.get("searchType")
        info_type = request.form.get("infoType")
        query = request.form.get("query").strip()

        try:
            if search_type == "username":
                res = requests.get(ROBLOX_API_USERNAME.format(query))
                res_json = res.json()
                if not res_json.get("Id"):
                    error = "Игрок не найден"
                    return render_template("index.html", data=None, error=error)
                user_id = res_json["Id"]
            else:
                user_id = query

            user_res = requests.get(ROBLOX_API_USER.format(user_id))
            user_data = user_res.json()
            data = {"ID": user_data.get("id"), "Username": user_data.get("name"), "DisplayName": user_data.get("displayName")}

            # Дополнительная информация
            if info_type == "inventory":
                inv_res = requests.get(f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles")
                data["Inventory"] = inv_res.json().get("data", [])
            elif info_type == "friends":
                friends_res = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends")
                data["Friends"] = friends_res.json().get("data", [])
            elif info_type == "groups":
                groups_res = requests.get(f"https://groups.roblox.com/v2/users/{user_id}/groups/roles")
                data["Groups"] = groups_res.json().get("data", [])
            elif info_type == "badges":
                badges_res = requests.get(f"https://badges.roblox.com/v1/users/{user_id}/badges")
                data["Badges"] = badges_res.json().get("data", [])
        except Exception as e:
            error = str(e)

    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
