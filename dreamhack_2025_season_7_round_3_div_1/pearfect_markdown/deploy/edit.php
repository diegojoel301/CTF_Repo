<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Markdown File</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>Edit Markdown File</h1>
        <form action="save.php" method="post">
            <textarea name="content" id="content" rows="20" cols="80"><?php
            $uploads_dir = 'uploads/';

            if (isset($_GET['file'])) {
                $file = $_GET['file'];
                $path = realpath($uploads_dir . $file);

                if (strpos($path, realpath($uploads_dir)) === 0 && file_exists($path)) {
                    echo htmlspecialchars(file_get_contents($path));
                } else {
                    echo "Invalid file or file not found!";
                }
            } else {
                echo "No file parameter provided!";
            }
            ?></textarea>
            <input type="hidden" name="file" value="<?php echo htmlspecialchars($_GET['file']); ?>">
            <input type="submit" value="Save">
        </form>
        <div class="markdown-preview" id="preview"></div>
    </div>
    <script>
        document.getElementById('preview').innerHTML = marked.parse(document.getElementById('content').value);
        document.getElementById('content').addEventListener('input', function() {
            document.getElementById('preview').innerHTML = marked.parse(this.value);
        });
    </script>
</body>
</html>
