"use strict";

function RecorderHookup(record, stop, counter, callback) {
    URL = window.URL || window.webkitURL;
    let gumStream;
    //stream from getUserMedia()
    let rec;
    //Recorder.js object
    let input;
    //MediaStreamAudioSourceNode we'll be recording
    // shim for AudioContext when it's not avb.
    let AudioContext = window.AudioContext || window.webkitAudioContext;
    let audioContext = new AudioContext;
    let constraints = {
        audio: true,
        video: false
    };

    let interval_n = undefined;

    record.onclick = function () {
        /* Disable the record button until we get a success or fail from getUserMedia() */

        record.disabled = true;
        stop.disabled = false;

        /* We're using the standard promise based getUserMedia()

        https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia */

        navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
            console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
            audioContext = new AudioContext();
            gumStream = stream;
            input = audioContext.createMediaStreamSource(stream);
            rec = new Recorder(input, {numChannels: 1});
            rec.record();

            console.log("Recording started");
        }).catch(function (err) {
            //enable the record button if getUserMedia() fails
            record.disabled = false;
            record.disabled = true;
        });
        counter.style.display = "unset";
        counter.innerText = "00:00";
        let length_seconds = 0;
        interval_n = setInterval(function () {
            length_seconds += 1;
            counter.innerText = Math.floor(length_seconds / 60).toString().padStart(2, "0") + ":" +
                (length_seconds % 60).toString().padStart(2, "0");
        }, 1000);
    };
    stop.onclick = function () {
        console.log("stopButton clicked");
        //disable the stop button, enable the record too allow for new recordings
        stop.disabled = true;
        record.disabled = false;

        clearInterval(interval_n);
        //tell the recorder to stop the recording
        rec.stop(); //stop microphone access
        gumStream.getAudioTracks()[0].stop();
        //create the wav blob and pass it on to createDownloadLink
        rec.exportWAV(callback);
    };
}

function Pohui() {
    let trainSendButton = document.getElementById("train-send");
    let recogSendButton = document.getElementById("recog-send");

    let trainBlob = undefined;
    let recogBlob = undefined;

    let trainSamplesLength = 0;
    let recogSamplesLength = 0;


    function saveRecording(name) {
        function save(blob) {
            if (name === "train") {
                trainBlob = blob;
                console.log(trainBlob);
                trainSendButton.disabled = false;
            }
            if (name === "recog") {
                recogBlob = blob;
                console.log(recogBlob);
                recogSendButton.disabled = false;
            }
        }

        return {save: save};
    }

    RecorderHookup(document.getElementById("train-record"),
        document.getElementById("train-stop"),
        document.getElementById("train-counter"),
        saveRecording("train").save);

    RecorderHookup(document.getElementById("recog-record"),
        document.getElementById("recog-stop"),
        document.getElementById("recog-counter"),
        saveRecording("recog").save);

    trainSendButton.onclick = function () {
        let gender = document.getElementById("train-gender").value;
        let age = document.getElementById("train-age").value;
        let name = document.getElementById("train-name").value;
        var fd = new FormData();
        console.log(trainBlob.size);
        fd.append('voice', trainBlob, "voice.wav");
        fd.append('name', name);
        fd.append('age', age);
        fd.append('gender', gender);
        trainSendButton.disabled = true;
        document.getElementById("loading").style.display = "unset";
        $.ajax({
            type: "POST",
            url: "/api/register",
            data: fd,
            cache: false,
            processData: false,
            contentType: false,
            error: function (error) {
                console.log(error);
                if (error.status === 400)
                    alert(error.responseText);
                else
                    alert("Что-то пошло не так\n" + error.statusText);
                document.getElementById("loading").style.display = "none";
                trainSendButton.disabled = false;
            }
        }).done(function (data) {
            console.log(data);
            let new_row = document.createElement("tr");
            let col_number = document.createElement("td");
            col_number.innerText = ++trainSamplesLength;
            let col_who = document.createElement("td");
            col_who.innerText = `${name} (${age} ${["Man", "Woman"][gender]})`
            let col_status = document.createElement("td");
            col_status.innerText = data;
            new_row.append(col_number, col_who, col_status);
            document.getElementById("train-records").appendChild(new_row);
            document.getElementById("loading").style.display = "none";
        });
    };

    recogSendButton.onclick = function () {
        var fd = new FormData();
        console.log(recogBlob.size);
        fd.append('voice', recogBlob, "voice.wav");
        fd.append('age', '20');
        fd.append('gender', '0');
        recogSendButton.disabled = true;
        document.getElementById("loading").style.display = "unset";
        $.ajax({
            type: "POST",
            url: "/api/recognize",
            data: fd,
            cache: false,
            processData: false,
            contentType: false,
            error: function (error) {
                console.log(error);
                if (error.status === 400)
                    alert(error.responseText);
                else
                    alert("Что-то пошло не так\n" + error.statusText);
                document.getElementById("loading").style.display = "none";
                recogSendButton.disabled = false;
            }
        }).done(function (data) {
            console.log(data);
            let new_row = document.createElement("tr");
            let col_number = document.createElement("td");
            col_number.innerText = ++recogSamplesLength;
            let col_result = document.createElement("td");
            col_result.innerText = data;
            let col_status = document.createElement("td");
            col_status.innerText = "ok";
            new_row.append(col_number, col_result, col_status);
            document.getElementById("recog-records").appendChild(new_row);
            document.getElementById("loading").style.display = "none";
        });
    }
}

document.addEventListener("DOMContentLoaded", Pohui);