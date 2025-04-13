<!DOCTYPE HTML>
<html lang="en">

<head>
    <title>Eldoria Cyber Attack</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">

    <!-- Include RPGUI styles and scripts -->
    <link href="rpgui/rpgui.min.css" rel="stylesheet" type="text/css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    <script src="rpgui/rpgui.min.js"></script>

    <style>
        body {
            background: #aaf;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: auto;
        }
    
        .rpgui-container {
            height: auto;
            max-width: 100%;
            width: 600px;
            margin: 3px auto;
            padding: 20px;
            position: relative;
            box-sizing: border-box;
        }
    
        .attack-buttons {
            
        }
    
        .attack-buttons button {
            margin: 10px;
            position: relative;
        }


        .results {
            margin-top: 20px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.5);
            color: white;
            border: 2px solid #fff;
            display: none;
        }
    
        .lore {
            text-align: center;
            margin-bottom: 20px;
        }
    
        .sword-image {
            position: absolute;
            width: 50px;
            height: 50px;
        }
    
        .sword-left {
            top: 10px;
            left: -60px;
        }
    
        .sword-right {
            top: 10px;
            right: -60px;
        }
    </style>
</head>

<body>
    <div class="rpgui-content">
        <!-- Main container -->
        <div class="rpgui-container framed">
            <img src="rpgui/img/icons/sword.png" class="sword-image sword-left" alt="Sword">
            <img src="rpgui/img/icons/sword.png" class="sword-image sword-right" alt="Sword">
            <h1>Welcome to Eldoria Cyber Attack</h1>
            <hr class="golden">

            <!-- Lore Section -->
            <div class="lore">
                <p>Rise, loyal servants of the Dark Ruler! The resistance believes they can stand against us. Prove them wrong. Use this weapon to strike down the so-called "heroes" of light. Let their hope turn to ash as they realize the futility of their struggle. The time has come to show them true darkness.</p>
                <p>Custom attacks are only allowed for Malakar's trusted servants.</p>
            </div>

            <!-- Player Name Input -->
            <label for="user-name">Enter Your Name:</label>
            <input type="text" id="user-name" name="user-name" placeholder="Name" required>
            <br><br>

            <!-- Target Input -->
            <label for="target">Enter Domain or IP:</label>
            <input type="text" id="target" name="target" placeholder="Domain or IP" required>
            <br><br>

            <hr class="golden">

            <!-- Attack Buttons -->
            <div class="attack-buttons">
                <button class="rpgui-button golden" id="attack-domain" disabled><p>Attack a Domain</p></button>
                <button class="rpgui-button golden" id="attack-ip" disabled ><p>Attack an IP</p></button>
            </div>

            <!-- Results Display -->
            <div class="results" id="results">
                <p>Results will appear here...</p>
            </div>
        </div>
    </div>

    <script>

        <?php 
            if (isset($_GET['result'])) {
                $result = $_GET['result'];
                echo "document.getElementById('results').innerHTML = '<p style=\"color: green;\">$result</p>';";
                echo "document.getElementById('results').style.display = 'block';";
            }
            if (isset($_GET['error'])) {
                $error = $_GET['error'];
                echo "document.getElementById('results').innerHTML = '<p style=\"color: red;\">$error</p>';";
                echo "document.getElementById('results').style.display = 'block';";
            }
        ?>
        
        // Check if the user's IP is local
        const isLocalIP = (ip) => {
            return ip === "127.0.0.1" || ip === "::1" || ip.startsWith("192.168.");
        };

        // Get the user's IP address
        const userIP = "<?php echo $_SERVER['REMOTE_ADDR']; ?>";

        // Enable/disable the "Attack IP" button based on the user's IP
        const attackIPButton = document.getElementById("attack-ip");

        // Enable buttons if required fields are filled
        const enableButtons = () => {
            const playerName = document.getElementById("user-name").value;
            const target = document.getElementById("target").value;
            const attackDomainButton = document.getElementById("attack-domain");
            const attackIPButton = document.getElementById("attack-ip");

            if (playerName && target) {
                attackDomainButton.disabled = false;
                attackDomainButton.removeAttribute("data-hover");
                if (isLocalIP(userIP)) {
                    attackIPButton.disabled = false;
                }
            } else {
                attackDomainButton.disabled = true;
                attackIPButton.disabled = true;
            }
        };

        document.getElementById("user-name").addEventListener("input", enableButtons);
        document.getElementById("target").addEventListener("input", enableButtons);

        // Attack Domain Button Click Handler
        document.getElementById("attack-domain").addEventListener("click", async () => {
            const target = document.getElementById("target").value;
            const name = document.getElementById("user-name").value;
            if (target) {
                window.location.href = `cgi-bin/attack-domain?target=${target}&name=${name}`;
            }
        });

        // Attack IP Button Click Handler
        document.getElementById("attack-ip").addEventListener("click", async () => {
            const target = document.getElementById("target").value;
            const name = document.getElementById("user-name").value;
            if (target) {
                window.location.href = `cgi-bin/attack-ip?target=${target}&name=${name}`;
            }
        });
    </script>
</body>

</html>