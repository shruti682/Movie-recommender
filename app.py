from flask import Flask, render_template, request
import recommend

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    list = recommend.getmovies()
    req_movie_details=[]
    if request.method == "POST":
        selectedmovie = request.form['selectedmovie']
        req_movie_details=recommend.recom(selectedmovie)
    return render_template("index.html",movie=list,details=req_movie_details)

if __name__ == "__main__":
	app.run()
