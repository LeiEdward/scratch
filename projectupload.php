<?php

if (move_uploaded_file($_FILES['import_file']['tmp_name'], './tmp/'.$_FILES['import_file']['name'])) {
  $sCont = file_get_contents ('tmp/'.$_FILES['import_file']['name']);
  $vProject =  json_decode($sCont, true);

  print_r($vProject);
}
else {
  echo 'NO';
}
