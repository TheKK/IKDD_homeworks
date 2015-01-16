var lineData = [];
var status_1 = -1;
var status_2 = -1;
var lineFunction = d3.svg.line()
                        .x(function(d) { return d.x; })
                        .y(function(d) { return d.y; })
                        .interpolate("linear");
var svgContainer;
var lineGraph1;
var lineGraph2;
var line_amounts = 0;
    function load(){

        svgContainer = d3.select("svg")
        draw_data();
        lineGraph1 = svgContainer.append("path")
        lineGraph2 = svgContainer.append("path")
        change_1();
    }
    function change_1(){
        status_1 = (status_1 + 1) % 5;
        status_2 = (status_2 + 1) % 5;
        if (line_amounts == 1){
            line_amounts = 0;
            status_1 = 0;
            status_2 = 0;
        }
        calc_line();
        draw_line();

        //line_amounts = (line_amounts + 1) % 2;
        //line_amounts = (line_amounts + 1) % 2
    }
    function change_21(){
        status_1 = (status_1 + 1) % 5;
        if (line_amounts == 0){
            line_amounts = 1;
            status_1 = 0;
            status_2 = 0;
        }
        calc_line();
        draw_line();
        //console.log(this)

        //status_2 = (status_2 + 1) % 8;
        //line_amounts = (line_amounts + 1) % 2;
        //line_amounts = (line_amounts + 1) % 2
    }
    function change_22(){
        status_2 = (status_2 + 1) % 8;
        if (line_amounts == 0){
            line_amounts = 1;
            status_1 = 0;
            status_2 = 0;
        }
        calc_line();
        draw_line();
        //console.log(this)
        //status_1 = (status_2 + 1) % 5;

        //line_amounts = (line_amounts + 1) % 2;
        //line_amounts = (line_amounts + 1) % 2
    }
    function calc_line(){
        var totalY;
        var count = 0;
        var c = new Coef(line_amounts, status_1, status_2);
        for (var i=-10; i<0; i+=0.01){
            totalY = 0;
            for (var j=0; j<c.theta1.length; j++){
                totalY += c.theta1[j] * Math.pow(i, j);
            }
            lineData[count] = {"x": i, "y":totalY};
            count += 1;
        }
        for (var i=0; i<10; i+=0.01){
            totalY = 0;
            for (var j=0; j<c.theta2.length; j++){
                if (status_2 >= 5 && line_amounts == 1){
                    if (j == 0)totalY += c.theta2[j];
                    else totalY += c.theta2[j] * Math.pow(i, 1/(j+1));
                }
                else{
                    totalY += c.theta2[j] * Math.pow(i, j);
                }
            }
            lineData[count] = {"x": i, "y":totalY};
            count += 1;
        }
        for (var i=0; i<lineData.length; i++){
            lineData[i].x = lineData[i].x * 40 + 400;
            lineData[i].y = lineData[i].y * 40 + 400;
        }
    }
    function draw_line(){
        lineGraph1.transition().attr("d", lineFunction(lineData.slice(0, lineData.length/2)))
                            .attr("stroke", "blue")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
        lineGraph2.transition().attr("d", lineFunction(lineData.slice(lineData.length/2, lineData.length)))
                            .attr("stroke", "blue")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
    }
    function draw_data(){
        for (var i=0; i<dataset.length; i++){
            dataset[i].X = dataset[i].X * 40 + 400;
            dataset[i].Y = dataset[i].Y * 40 + 400;
            var x = svgContainer.append("circle")
            .attr("r", 3)
            .attr("cx", dataset[i].X)
            .attr("cy", dataset[i].Y)
            .attr("fill", "red");
        }
    }
