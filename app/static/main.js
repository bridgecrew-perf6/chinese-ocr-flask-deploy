//========================================================================
// Drag and drop image handling
//========================================================================

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

// Add event listeners
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  // prevent default behaviour
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}


$('#image-url').change(function(){
  imagePreview.src = $(this).val();
  show(imagePreview);
  hide(uploadCaption);
  
  // reset
  predResult.innerHTML = "";
  imagePreview.classList.remove("loading");
  
    
}

)

//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreview = document.getElementById("image-preview");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-table");
var loader = document.getElementById("loader");

//========================================================================
// Main button events
//========================================================================

function submitImage() {
  // action for the submit button
  if (!imagePreview.src ) {
    window.alert("Please select an image before submit.");
    return;
  }

  loader.classList.remove("hidden");
  imagePreview.classList.add("loading");

  // call the predict function of the backend
  predictImage(imagePreview.src);
}

function clearImage() {
  // reset selected files
  fileSelect.value = "";
  $('#image-url').val('');
  // remove image sources and hide them
  imagePreview.src = "";
  predResult.innerHTML = "";

  hide(imagePreview);
  hide(loader);
  hide(predResult);
  show(uploadCaption);

  imagePreview.classList.remove("loading");
}

function previewFile(file) {
  // show the preview of the image
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    // reset
    predResult.innerHTML = "";
    imagePreview.classList.remove("loading");

    displayImage(reader.result, "image-preview");
  };
}

//========================================================================
// Helper functions
//========================================================================

function predictImage(image) {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayImage(data.image, "image-preview");
          displayResult(data);
          imagePreview.classList.remove("loading");
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}


function displayImage(image, id) {
  // display image on given id <img> element
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  // display the result    
  result = `
  <thead>
  <tr>
  <th>
     Text  
  </th>
  <th>
    Prob
  </th>
  </tr>
</thead>
<tbody>
  `
  for ( i=0 ; i<data.result.length ; i++ )
  {   
      result += `<tr><td>${data.result[i].text}</td>
                <td>${data.result[i].textprob}</td></tr>`
  }

  hide(loader);
  predResult.innerHTML = result+'</tbody>';
  show(predResult);
}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}

