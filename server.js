const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

let currentMultiplier = 1.00;
let isGameRunning = false;

function gameLoop() {
    isGameRunning = true;
    currentMultiplier = 1.00;
    const crashPoint = (Math.random() * 4 + 1.2).toFixed(2); // 1.2x dan 5.2x gacha crash

    let interval = setInterval(() => {
        currentMultiplier += 0.01;
        io.emit('tick', currentMultiplier.toFixed(2));

        if (currentMultiplier >= crashPoint) {
            clearInterval(interval);
            io.emit('crash', crashPoint);
            isGameRunning = false;
            setTimeout(gameLoop, 5000); // 5 soniyadan keyin yangi raund
        }
    }, 100);
}

gameLoop();
http.listen(3000, () => console.log('Server 3000-portda ishlamoqda'));
