<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Markdown Editor</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>Upload and Edit Markdown Files</h1>
        <form action="upload.php" method="post" enctype="multipart/form-data">
            <label for="file">Choose Markdown file:</label>
            <input type="file" name="file" id="file" accept=".md">
            <input type="submit" value="Upload">
        </form>

        <div class="preview-container">
            <h2>Example Markdown Preview</h2>
            <div class="markdown-preview" id="preview"></div>
        </div>

        <?php
        $uploads_dir = 'uploads/';
        if ($handle = opendir($uploads_dir)) {
            echo "<h2>Uploaded Files</h2><ul>";
            while (false !== ($entry = readdir($handle))) {
                if ($entry != "." && $entry != "..") {
                    echo "<li><a href='edit.php?file=" . urlencode($entry) . "'>" . htmlspecialchars($entry) . "</a></li>";
                }
            }
            closedir($handle);
            echo "</ul>";
        }
        ?>
    </div>
    <script>
        fetch('post_handler.php')
        .then(response => response.text())
        .then(data => {
            document.getElementById('preview').innerHTML = marked.parse(data);
        });
    </script>
</body>
</html>
