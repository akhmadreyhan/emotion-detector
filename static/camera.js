const video = document.getElementById('video');
const captureBtn = document.getElementById('capture-btn');
const inputimg = document.getElementById('image');

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: {ideal:640},
                height: {ideal:480}
            }
        });

        video.srcObject = stream;
    } catch (err) {
        alert("Failed to access camera: " + err);
    }
}

startCamera();
captureBtn.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL('image/jpeg', 0.9);
    inputimg.value = imageData;
    document.getElementById('upload-form').submit();
});