function drawBoulder(svgElementId, svgWidth, svgHeight, clickable, boulderData) {
    const skip = [
        10, 21, 32, 33, 42, 47, 62, 67, 84, 89, 104, 109, 126, 131, 146,
        151, 168, 173, 188, 193, 202, 211, 216, 231, 236, 253, 258, 273,
        278, 295, 300, 315, 320, 337, 342
    ];
    const colorsHoldType = {    
        "green": "holds_start",
        "blue": "holds_general",
        "red": "holds_finish",
        "purple": "holds_feet_only",
        "yellow": "holds_hands_only",
        "gray": "none"
    };
    const holdTypeColors = Object.fromEntries(Object.entries(colorsHoldType).map(([key, value]) => [value, key]));
    const svgElement = document.getElementById(svgElementId);
    const rows = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T'];
    const baseCircleOpacity = "0.2";
    const baseCircleFill = "gray";
    let hold_number = 0;

    const dimensions = computeDimensions(svgWidth, svgHeight, 10, 20, 40);

    svgElement.setAttribute("width", dimensions.svgWidth);
    svgElement.setAttribute("height", dimensions.svgHeight);
    let y_cord = dimensions.svgHeight - 10 * dimensions.verticalScale;
    let x_cord = dimensions.svgWidth - 8 * dimensions.horizontalScale;

    // Draws the kickboard.
    for (let i = 0; i < 30; i++) {
        while (skip.includes(hold_number)) { hold_number += 1; }
        if (i % 2 == 1) {
            y_cord = dimensions.svgHeight - 10 * dimensions.verticalScale;
        } else {
            y_cord = dimensions.svgHeight - 20 * dimensions.verticalScale;
        }
        drawHoldCircle(svgElement, x_cord, y_cord, dimensions.circleRadius/2, baseCircleFill, baseCircleOpacity,
            hold_number, clickable, boulderData) 
        x_cord -= (dimensions.svgWidth - dimensions.horizontalOffset) / 30;
        hold_number += 1;
    }

    // Draws the wall. First line on the bottom left goes up. Then we loop one line down next line up.
    y_cord = dimensions.svgHeight - 40 * dimensions.verticalScale;
    x_cord = 12 * dimensions.horizontalScale + dimensions.horizontalOffset;
    while (y_cord >= 0) {
        while (skip.includes(hold_number)) { hold_number += 1; }
        drawHoldCircle(svgElement, x_cord, y_cord, dimensions.circleRadius, baseCircleFill, baseCircleOpacity,
            hold_number, clickable, boulderData)
        let letter = document.createElementNS("http://www.w3.org/2000/svg", "text");
        letter.setAttribute("x", x_cord - dimensions.horizontalOffset - 4 * dimensions.horizontalScale);
        letter.setAttribute("y", y_cord + 5 * dimensions.verticalScale);
        letter.setAttribute("font-size", "13");
        letter.setAttribute("fill", "black");
        letter.setAttribute("class", "coordinates");
        letter.textContent = rows.shift();
        svgElement.appendChild(letter);
        hold_number += 1;
        y_cord -= (dimensions.svgHeight - 40 * dimensions.verticalScale) / 19;
    }

    for(let i = 0; i < 7; i ++) {

        x_cord += (dimensions.svgWidth - dimensions.horizontalOffset) / 15
        y_cord += (dimensions.svgHeight - 40 * dimensions.verticalScale) / 19;
        while (y_cord <= dimensions.svgHeight - 40 * dimensions.verticalScale) {
            while (skip.includes(hold_number)) { hold_number += 1; }
            drawHoldCircle(svgElement, x_cord, y_cord, dimensions.circleRadius, baseCircleFill, baseCircleOpacity,
                hold_number, clickable, boulderData) 
            hold_number += 1;
            y_cord += (dimensions.svgHeight - 40 * dimensions.verticalScale) / 19;
        }

        y_cord -= (dimensions.svgHeight - 40 * dimensions.verticalScale) / 19
        x_cord += (dimensions.svgWidth - dimensions.horizontalOffset) / 15
        while (y_cord >= 0) {
            while (skip.includes(hold_number)) { hold_number += 1; }
            drawHoldCircle(svgElement, x_cord, y_cord, dimensions.circleRadius, baseCircleFill, baseCircleOpacity,
                hold_number, clickable, boulderData) 
            hold_number += 1;
            y_cord -= (dimensions.svgHeight - 40 * dimensions.verticalScale) / 19;
        }
    }

    // Draws the numbers on the top.
    y_cord = 10 * dimensions.verticalScale;
    x_cord = 12 * dimensions.horizontalScale + dimensions.horizontalOffset - 5 * dimensions.horizontalScale;
    for(let i = 1; i <= 15; i++) {
        let num = document.createElementNS("http://www.w3.org/2000/svg", "text");
        num.setAttribute("x", x_cord);
        num.setAttribute("y", y_cord);
        num.setAttribute("font-size", "13");
        num.setAttribute("fill", "black");
        num.setAttribute("class", "coordinates");
        num.textContent = i;
        svgElement.appendChild(num);
        if (i == 9) { x_cord -= 3 * dimensions.horizontalScale; } // Centering the double digit numbers.
        x_cord += (dimensions.svgWidth - dimensions.horizontalOffset) / 15;
    }
    
    console.log(JSON.stringify(boulderData, null, 2));
    if(boulderData) {
        for (const [holdType, holds] of Object.entries(boulderData)) {
            const color = holdTypeColors[holdType];
            for (const hold of holds) {
                let circle = document.getElementById("hold-" + hold);
                if (circle) {
                    console.log("color:" + color)
                    console.log([holdType, holds]);
                    circle.setAttribute("fill", color);
                    circle.setAttribute("opacity", "0.6");
                }
            }
        }
    }
};

function computeDimensions(svgBaseWidth, svgBaseHeight, circleRadius, horizontalOffset, verticalOffset) {
    let deviceWidth = window.innerWidth;
    let deviceHeight = window.innerHeight;
    let computedHorizontalOffset;
    let computedVerticalOffset; 
    let computedCircleRadius;
    let svgWidth;
    let svgHeight;
    let verticalScale;
    let horizontalScale;

    if (deviceWidth < 500 ) {
        svgWidth = deviceWidth * 0.9;
        svgHeight = svgWidth * (svgBaseHeight / svgBaseWidth);
        computedHorizontalOffset = svgWidth * (horizontalOffset / svgBaseWidth);
        computedVerticalOffset = svgHeight * (verticalOffset / svgBaseHeight);
        computedCircleRadius = svgWidth * (circleRadius / svgBaseWidth);
        verticalScale = svgHeight / svgBaseHeight;
        horizontalScale = svgWidth / svgBaseWidth;
    } else {
        computedHorizontalOffset = horizontalOffset;
        computedVerticalOffset = verticalOffset;
        computedCircleRadius = circleRadius;
        svgWidth = svgBaseWidth;
        svgHeight = svgBaseHeight;
        verticalScale = 1;
        horizontalScale = 1;
    }

    return {
        horizontalOffset: computedHorizontalOffset,
        verticalOffset: computedVerticalOffset,
        circleRadius: computedCircleRadius,
        svgWidth: svgWidth,
        svgHeight: svgHeight,
        verticalScale: verticalScale,
        horizontalScale: horizontalScale
    };
}

function onCircleClick(event, colors, colorsHoldType) {
    const fillColor = event.target.getAttribute("fill");
    const currentColorIndex = colors.indexOf(fillColor);
    if (currentColorIndex == colors.length - 2) {
        event.target.setAttribute("opacity", "0.2");
    } else {
        event.target.setAttribute("opacity", "0.6");
    }
    event.target.setAttribute("fill", colors[(currentColorIndex + 1) % colors.length]);

    updateHoldFields(event, colorsHoldType, fillColor);
}

//Removes holdId from previous hold field and adds it to the new hold field.
function updateHoldFields(event, colorsHoldType, prevFillColor) {

    let holdId = parseInt(event.target.getAttribute("id").split("-")[1]);
    let prevHoldField = document.getElementById("id_" + colorsHoldType[prevFillColor]);
    if (prevHoldField) {
        // Remove holdId from previous hold field
        let prevHoldArray = JSON.parse(prevHoldField.value || '[]');
        prevHoldArray = prevHoldArray.filter(id => id !== holdId);
        prevHoldField.value = JSON.stringify(prevHoldArray);
    }  
    // Add holdId to new hold field if it's not gray.
    let holdField;
    let holdArray;
    if (event.target.getAttribute("fill") != "gray") {
        holdField = document.getElementById("id_" + colorsHoldType[event.target.getAttribute("fill")]);
        holdArray = JSON.parse(holdField.value || '[]');
        // Add holdId to new hold field if it's not already there
        if (!holdArray.includes(holdId)) {
            holdArray.push(holdId);
        }
        holdField.value = JSON.stringify(holdArray);
    }

    // Get all hold arrays
    const start = JSON.parse(document.getElementById("id_holds_start").value || '[]');
    const finish = JSON.parse(document.getElementById("id_holds_finish").value || '[]');
    const general = JSON.parse(document.getElementById("id_holds_general").value || '[]');
    const feet = JSON.parse(document.getElementById("id_holds_feet_only").value || '[]');
    const hands = JSON.parse(document.getElementById("id_holds_hands_only").value || '[]');

    // Update LEDs in real-time, only if light button is toggled.
    if (document.getElementById("light-button").classList.contains("on")) {
        lightBoulderFromCircle(start, finish, general, feet, hands);
    }
}

function drawHoldCircle(svgElement, x_cord, y_cord, radius, fillColor, opacity, holdNumber, clickable) {
    const colors = ["green", "blue", "red", "purple", "yellow", "gray"];
    const colorsHoldType = {    
        "green": "holds_start",
        "blue": "holds_general",
        "red": "holds_finish",
        "purple": "holds_feet_only",
        "yellow": "holds_hands_only",
    };
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", x_cord);
    circle.setAttribute("cy", y_cord);
    circle.setAttribute("r", radius);
    circle.setAttribute("stroke-width", "1");
    circle.setAttribute("stroke", "black");
    circle.setAttribute("fill", fillColor);
    circle.setAttribute("opacity", opacity);
    circle.setAttribute("id", "hold-" + holdNumber);
    if (clickable) {
        circle.addEventListener("click", (event) => onCircleClick(event, colors, colorsHoldType));
        circle.addEventListener("mouseover", (event) => {
            if (event.target.getAttribute("fill") == fillColor &&
                event.target.getAttribute("opacity") == opacity) {
                event.target.setAttribute("opacity", "0.4");
            }
        });
        circle.addEventListener("mouseout", (event) => {
            if (event.target.getAttribute("fill") == fillColor &&
                event.target.getAttribute("opacity") != opacity) {
                event.target.setAttribute("opacity", opacity);
            }
        });
    }
    svgElement.appendChild(circle);
}