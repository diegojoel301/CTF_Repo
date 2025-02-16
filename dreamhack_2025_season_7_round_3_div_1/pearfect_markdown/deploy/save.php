<?php
$uploads_dir = 'uploads/';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $file = $_POST['file'];
    $content = $_POST['content'];
    $path = realpath($uploads_dir . basename($file));

    if (strpos($path, realpath($uploads_dir)) === 0 && file_exists($path)) {
        file_put_contents($path, $content);
        header('Location: edit.php?file=' . urlencode($file));
        exit;
    } else {
        echo "Invalid file or file not found!";
    }
} else {
    echo "Invalid request method!";
}
?>
