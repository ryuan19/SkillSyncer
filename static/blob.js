console.clear();
                const shape = document.getElementById('shape')

                const radii = {
                top: 50,
                right: 50,
                bottom: 50,
                left: 50
                }

                const dx = {
                top: [],
                right: [],
                bottom: [],
                left: []
                }

                const formatBorderRadius = (top, right, bottom, left) => {
                return `${top}% ${100-top}% ${100-bottom}% ${bottom}% / ${left}% ${right}% ${100-right}% ${100-left}%`
                }

                const updateBorderRadius = (top, right, bottom, left) => {
                shape.style.borderRadius = formatBorderRadius(top, right, bottom, left);
                }

                const random = (x) => 2 * x * (0.5 - Math.random())

                const smoothChange = (x, dx) => {
                if (dx.length > 60) dx.shift();
                
                dx.push(random(5) + (50 - x)/20)
                
                x = x + dx.reduce((a,b) => a+b)/dx.length
                
                return [x, dx]
                }

                setInterval(() => {
                [radii.top, dx.top] = smoothChange(radii.top, dx.top);
                [radii.right, dx.right] = smoothChange(radii.right, dx.right);
                [radii.bottom, dx.bottom] = smoothChange(radii.bottom, dx.bottom);
                [radii.left, dx.left] = smoothChange(radii.left, dx.left);
                
                updateBorderRadius(
                    radii.top,
                    radii.right,
                    radii.bottom,
                    radii.left
                )
                }, 
                15
                )