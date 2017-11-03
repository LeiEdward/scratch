<?php


?>
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script>
$(function (){
  $('#btn_submit').click( function () {
    var fileupload = $('#fileupload').prop('files')[0];
    var form_data = new FormData();
    form_data.append('import_file', fileupload);
    console.log(fileupload, form_data);

    $.ajax({
        url: "projectupload.php",
        method: "POST",
        data: form_data,
        processData: false, // 告訴JQuery不要去處理發送的數據，不然會把data
                            //設置的物件轉換成查詢字符串以配合預設的application/x-www-form-urlencoded

        contentType: false, // 告訴JQuery不要去設置Content-Type請求Header，
                            //Header會自動適情況加上multipart/form-data
        success: function (response) {
            console.log(response);
        },
        error: function (jqXHR, textStatus, errorMessage) {
            console.log(errorMessage);
        }
    });
  });
});
</script>
</head>
<body>
    <div class="form-inline" style="width:800px;margin:0px auto;">
      <label for="fileupload">Scratch 專案分析</label>
      <input id="fileupload" type="file" class="form-control mb-2 mr-sm-2 mb-sm-0" />
      <button id="btn_submit" class="btn btn-primary">Submit</button>
    </div>
  </form>
</body>
</html>
