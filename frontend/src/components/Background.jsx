import { useEffect, useRef } from "react";


const NODE_COUNT = 55;
const CONNECTION_DISTANCE = 150;


export default function Background() {

    const canvasRef = useRef(null);


    useEffect(() => {

        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");

        let animationFrame;

        let mouse = {
            x: null,
            y: null,
        };


        function resizeCanvas() {

            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }


        resizeCanvas();

        window.addEventListener(
            "resize",
            resizeCanvas
        );


        const nodes = Array.from(
            { length: NODE_COUNT },
            () => ({

                x: Math.random() * window.innerWidth,

                y: Math.random() * window.innerHeight,

                vx: (Math.random() - 0.5) * 0.25,

                vy: (Math.random() - 0.5) * 0.25,

                radius: Math.random() * 1.5 + 1,
            })
        );


        function handleMouseMove(event) {

            mouse.x = event.clientX;
            mouse.y = event.clientY;
        }


        function handleMouseLeave() {

            mouse.x = null;
            mouse.y = null;
        }


        window.addEventListener(
            "mousemove",
            handleMouseMove
        );

        window.addEventListener(
            "mouseleave",
            handleMouseLeave
        );


        function draw() {

            ctx.clearRect(
                0,
                0,
                canvas.width,
                canvas.height
            );


            // -----------------------------------------
            // Move nodes
            // -----------------------------------------

            nodes.forEach((node) => {

                node.x += node.vx;
                node.y += node.vy;


                if (
                    node.x < 0 ||
                    node.x > canvas.width
                ) {

                    node.vx *= -1;
                }


                if (
                    node.y < 0 ||
                    node.y > canvas.height
                ) {

                    node.vy *= -1;
                }


                // Mouse interaction
                if (
                    mouse.x !== null &&
                    mouse.y !== null
                ) {

                    const dx = mouse.x - node.x;
                    const dy = mouse.y - node.y;

                    const distance = Math.sqrt(
                        dx * dx + dy * dy
                    );


                    if (distance < 130) {

                        node.x -= dx * 0.0008;
                        node.y -= dy * 0.0008;
                    }
                }

            });


            // -----------------------------------------
            // Connections
            // -----------------------------------------

            for (
                let i = 0;
                i < nodes.length;
                i++
            ) {

                for (
                    let j = i + 1;
                    j < nodes.length;
                    j++
                ) {

                    const a = nodes[i];
                    const b = nodes[j];

                    const dx = a.x - b.x;
                    const dy = a.y - b.y;

                    const distance = Math.sqrt(
                        dx * dx + dy * dy
                    );


                    if (
                        distance <
                        CONNECTION_DISTANCE
                    ) {

                        const opacity =
                            1 -
                            distance /
                            CONNECTION_DISTANCE;


                        ctx.beginPath();

                        ctx.moveTo(
                            a.x,
                            a.y
                        );

                        ctx.lineTo(
                            b.x,
                            b.y
                        );

                        ctx.strokeStyle =
                            `rgba(110, 140, 180, ${opacity * 0.16})`;

                        ctx.lineWidth = 1;

                        ctx.stroke();
                    }
                }
            }


            // -----------------------------------------
            // Nodes
            // -----------------------------------------

            nodes.forEach((node) => {

                let radius = node.radius;


                if (
                    mouse.x !== null &&
                    mouse.y !== null
                ) {

                    const dx =
                        mouse.x - node.x;

                    const dy =
                        mouse.y - node.y;

                    const distance =
                        Math.sqrt(
                            dx * dx +
                            dy * dy
                        );


                    if (distance < 100) {

                        radius +=
                            (1 - distance / 100) * 3;
                    }
                }


                ctx.beginPath();

                ctx.arc(
                    node.x,
                    node.y,
                    radius,
                    0,
                    Math.PI * 2
                );

                ctx.fillStyle =
                    "rgba(160, 190, 230, 0.7)";

                ctx.fill();
            });


            animationFrame =
                requestAnimationFrame(draw);
        }


        draw();


        return () => {

            cancelAnimationFrame(
                animationFrame
            );

            window.removeEventListener(
                "resize",
                resizeCanvas
            );

            window.removeEventListener(
                "mousemove",
                handleMouseMove
            );

            window.removeEventListener(
                "mouseleave",
                handleMouseLeave
            );
        };

    }, []);


    return (
        <canvas
            ref={canvasRef}
            className="background-canvas"
        />
    );
}