document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file_upload");
    const imagePreview = document.getElementById("image-preview");
  
    fileInput.addEventListener("change", function (event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
  
        reader.addEventListener("load", function () {
          imagePreview.src = reader.result;
          localStorage.setItem("imageData", reader.result);
        });
  
        reader.readAsDataURL(file);
      }
    });
  
    const imageData = localStorage.getItem("imageData");
    if (imageData) {
      imagePreview.src = imageData;
    }
  });
console.log("Sam")  