<?php
$uploads_dir = 'uploads/';
if ($_FILES['file']['error'] === UPLOAD_ERR_OK) {
    $tmp_name = $_FILES['file']['tmp_name'];
    $name = basename($_FILES['file']['name']);
    
    if (pathinfo($name, PATHINFO_EXTENSION) === 'md') {
        move_uploaded_file($tmp_name, "$uploads_dir/$name");
        echo "File uploaded successfully!";
    } else {
        echo "Only .md files are allowed!";
    }
} else {
    echo "File upload error!";
}
?>
