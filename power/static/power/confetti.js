window.onload = function() {
    const canvas = document.getElementById('confetti-canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const confetti = [];
    const confettiCount = 150;

    function random(min, max) {
        return Math.random() * (max - min) + min;
    }

    for (let i = 0; i < confettiCount; i++) {
        confetti.push({
            x: random(0, canvas.width),
            y: random(0, canvas.height),
            r: random(2, 6),
            d: random(1, 3),
            color: `hsl(${random(0, 360)}, 100%, 50%)`,
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        confetti.forEach(c => {
            ctx.beginPath();
            ctx.arc(c.x, c.y, c.r, 0, Math.PI * 2, false);
            ctx.fillStyle = c.color;
            ctx.fill();
        });

        update();
        requestAnimationFrame(draw);
    }

    function update() {
        confetti.forEach(c => {
            c.y += c.d;
            c.x += Math.sin(c.y * 0.05);

            if (c.y > canvas.height) {
                c.y = 0;
                c.x = random(0, canvas.width);
            }
        });
    }

    draw();
};
