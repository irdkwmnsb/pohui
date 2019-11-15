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
    let length_seconds = 0;

    counter.innerText = "00:00";

    record.onclick = function () {
        /* Disable the record button until we get a success or fail from getUserMedia() */

        record.disabled = true;
        stop.disabled = false;

        /* We're using the standard promise based getUserMedia()

        https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia */

        navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
            console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
            /* assign to gumStream for later use */
            gumStream = stream;
            /* use the stream */
            input = audioContext.createMediaStreamSource(stream);
            /* Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size */
            rec = new Recorder(input, {
                numChannels: 1
            });
            //start the recording process
            rec.record();
            console.log("Recording started");
        }).catch(function (err) {
            //enable the record button if getUserMedia() fails
            record.disabled = false;
            record.disabled = true;
        });
        interval_n = setInterval(function () {
            counter.innerText = Math.floor(length_seconds / 60).toString().padStart(2, "0") + ":" +
                (length_seconds % 60).toString().padStart(2, "0");
            length_seconds += 1;
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

    function saveRecording(name) {
        function save(blob) {
            if (name === "train") {
                trainBlob = blob;
            }
            if (name === "recog") {
                recogBlob = blob;
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

    function trainSend() {

    }

    function recogSend() {

    }
}

document.addEventListener("DOMContentLoaded", Pohui);