const url = "http://127.0.0.1:5000/api/v1/audio";
const lyricsurl = "http://127.0.0.1:5000/api/v1/lyrics";
let html_uploadButton, fileUploader;
let lyricsUploader;
let html_uploadLyricsButton;
let list = document.getElementById("myList");
html_error = document.querySelector(".js-error");

function uploadAudio(files) {

	let file = files[0];
    console.log(file);
	let formData = new FormData();
	formData.set('audio', file);
	formData.set('name', file.name);

	// make the POST request with the formdata as body
	fetch(url, {
		method: "POST",
        body: formData
	})
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            let i = 0;
            let artist = [];
            let song = [];
            let genre = [];
            for (const [key, value] of Object.entries(data)) {
                dict = value

                for (const [key, value] of Object.entries(dict)) {
                    i++;
                    if (i < 4) {
                        console.log(artist)
                        artist.push(value)
                    } else if (i < 7) {
                        genre.push(value)
                    } else {
                        song.push(value)
                }
                console.log(artist);
                console.log(genre);
                console.log(song);
              }
            }
            //   for (const [key, value] of Object.entries(data)) {
            //     console.log(key, value);
            //   }
			// return data;
            document.getElementById('lyricsResults').innerHTML = "The audio you provided leans towards the genre: " + genre[0];
            document.getElementById('Recommendations').innerHTML = "Here are three songs from the same predicted genre: ";
            document.getElementById('song1').innerHTML = song[0] + ' by: ' + artist[0];
            document.getElementById('song2').innerHTML = song[1] + ' by: ' + artist[1];
            document.getElementById('song3').innerHTML = song[2] + ' by: ' + artist[2];
		})
		.catch((error) => {
            // show error message
            document.getElementById('lyricsResults').innerHTML = "Something went wrong please make sure you uploaded a .wav file!";
			// showError(error);
		});
}

function uploadLyrics(lyrics) {
    console.log(lyrics);
	// make the POST request with the formdata as body
	fetch(lyricsurl, {
		method: "POST",
        body: lyrics
	})
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            let i = 0;
            let artist = [];
            let song = [];
            let genre = [];
            for (const [key, value] of Object.entries(data)) {
                dict = value

                for (const [key, value] of Object.entries(dict)) {
                    i++;
                    if (i < 4) {
                        console.log(artist)
                        artist.push(value)
                    } else if (i < 7) {
                        genre.push(value)
                    } else {
                        song.push(value)
                }
                console.log(artist);
                console.log(genre);
                console.log(song);
              }
            }
            //   for (const [key, value] of Object.entries(data)) {
            //     console.log(key, value);
            //   }
			// return data;
            document.getElementById('lyricsResults').innerHTML = "The lyrics you provided lean towards the genre: " + genre[0];
            document.getElementById('Recommendations').innerHTML = "Here are three songs from the same predicted genre: ";
            document.getElementById('song1').innerHTML = song[0] + ' by: ' + artist[0];
            document.getElementById('song2').innerHTML = song[1] + ' by: ' + artist[1];
            document.getElementById('song3').innerHTML = song[2] + ' by: ' + artist[2];
            // document.getElementById('Recommendations').innerHTML = "Here are 3 songs in the same genre for you:  "+ data;
		})
		.catch((error) => {
            // show error message
            document.getElementById('lyricsResults').innerHTML = "Something went wrong please try again!";
		});
}


/**
 * Simple error alert
 */


function listenToElements() {
	// uploader
    html_uploadButton = document.querySelector(".js-upload-button");
    fileUploader = document.querySelector(".js-upload-input");
    html_uploadLyricsButton = document.querySelector(".js-upload-lyrics-button");
    lyricsUploader = document.querySelector(".js-upload-lyrics");
    // listeners
	// when clicking on the button, open the file uploader menu
	// if a video in the file uploader menu is chosen, upload it
    html_uploadButton.addEventListener("click", (e) => {
		e.preventDefault();
		fileUploader.click();
	});
    fileUploader.addEventListener("change", (e) => {
        e.preventDefault();
        let files = e.target.files;
        if (files) {
            uploadAudio(files);
        }
    });
    html_uploadLyricsButton.addEventListener("click", (e) => {
        e.preventDefault();
        let lyrics = prompt("Please enter the lyrics, the more you enter the better the result!");
        if (lyrics == null || lyrics == "") {
            alert("You must enter some lyrics!");
        } else {
            console.log(lyrics);
            uploadLyrics(lyrics);
        }
	});
}

 document.addEventListener("DOMContentLoaded", () => {
	console.log("DOMContentLoaded");
	listenToElements();
});
