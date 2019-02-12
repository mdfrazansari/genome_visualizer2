class GenomeSlider {
    constructor(container, idSuffix, pqArmData) {
        this.config = {
            margin: {top: 20, right: 20, bottom: 30, left: 40},
            extraPaddingRight: 100,
            brushWidth: 200,
        }

        this.svgSelector = ".svg-" + idSuffix;
        this.idSuffix = idSuffix;
        var svgCreator = "<div class='row'><div class='col-md-11'><svg class='scaling-svg svg-" + idSuffix + "' height='120' width='110'>" +
                "<defs>" +
                    "<clipPath id='mask-" + idSuffix +"'>" +
                      "<rect x='0' y='0' width='" + this.getWidth() + "' height='" + (this.getHeight() + this.config.margin.top) + "' />"+
                    "</clipPath>" +
                "</defs></svg></div><div class='col-md-1'><button tabindex=-1 class='btn-" + idSuffix +"' style='color: blue; margin-top:" + this.getHeight() +"px'><i class='fas fa-search-plus'></i></button></div></div>";
        container.append($(svgCreator));
        this.container = container;
        this.svg = d3.select(this.svgSelector);
        this.x = d3.scaleLinear().rangeRound([0, this.getWidth()])
        this.y = d3.scaleBand().rangeRound([this.getHeight(), 0]).padding(0.1);
        this.g = this.svg.append("g")
            .attr("class", "chart")
            .attr('clip-path', "url(#mask-" + idSuffix + ")")
            .attr("transform", "translate(" + this.config.margin.left + "," + this.config.margin.top + ")");
        this.brush = d3.brushX()
            .extent([[0, 0], [this.getWidth(), this.getHeight()]])
            .on("start brush", () => this.brushed(this));
        this.bisectVariation = d3.bisector(function(d) { return d.POS; }).left;
        $(".btn-"+idSuffix).click(() => this.test(this));
        this.layers = [1, 2, 3]
        
    }
    
    draw() {
        gs = this;
        var layer1 = new Layer(gs, 1, "chrY", pqlayerfn);
        var layer2 = new Layer(gs, 2, "chrY", cytobandlayerfn);
        var layer3 = new Layer(gs, 3, "chrY", variationlayerfn);
        layer1.setNextLayer(layer2);
        layer2.setNextLayer(layer3);
        layer1.render();
    }

    
    test() {
        if(!this.gs) {
            this.addChildLevel();
        }
    }

    empty() {
        $('.chart', $(this.svgSelector)).empty();
    }

    setXDomain(extent) {
        this.x.domain(extent);
        this.g.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + this.getHeight() + ")")
            .call(d3.axisBottom(this.x));
    }

    setYDomain(extent) {
        this.y.domain(extent);
        $(".axis--y", $(this.svgSelector)).remove();
        this.svg.append("g")
          .attr("class", "axis axis--y")
          .attr("transform", "translate(" + this.config.margin.left + "," + this.config.margin.top + ")")
          .call(d3.axisLeft(this.y));
    }

    renderPQBand(data) {
        
    }

    renderCytoBand(data) {
        this.cbd = data;
        var bands_g = this.g.append("g").attr('class', "bands");
        var x = this.x;
        var y = this.y;
        var bands = bands_g.selectAll("rect")
              .data(data)
              .enter()
              .append("rect")
              .attr("class", "bar")
              .attr("x",  function(d) { return x(d.chromStart)})
              .attr("y", function(d, i) {return y(d.chrom) + y.bandwidth()/4; })
              .attr("height", function(d, i) {return  y.bandwidth()/2; })
              .attr("width", function(d) {return x(d.chromEnd) - x(d.chromStart);})
              .attr("fill", function(d) {
                if(d.gieStain=='gneg') {//gneg', 'gpos25', 'gpos50', 'gpos75', 'gpos100', 'acen', 'gvar','stalk
                  return "#9d1cb2";
                } else if (d.gieStain=='gpos25') {
                  return "#cdde20";
                } else if (d.gieStain=='gpos50') {
                  return "#ffc200";
                } else if (d.gieStain=='gpos75') {
                  return "#ff9900";
                } else if (d.gieStain=='gpos100') {
                  return "#7a5547";
                } else if (d.gieStain=='acen') {
                  return "#5f7d8c";
                } else if (d.gieStain=='gvar') {
                  return "#9e9e9e";
                } else if (d.gieStain=='stalk') {
                  return "#ec1261";
                }
              });
    }

    renderVariations(variationData) {
        this.vd = variationData;
        var x = this.x;
        var y =this.y;
        var variations_g = this.g.append("g").attr("class", "variations");
        variations_g.selectAll("circle")
        .data(variationData)
        .enter()
        .append("rect")
        .attr("class", "tabbable-rect")
        .attr("y", function(d) {return (y(d.CHROM));})
        .attr("x", function(d) {return x(d.POS)})
        .attr("data-x", function(d) {return d.POS})
        .attr("height", y.bandwidth())
        .attr("width", 1)
        .attr("tabindex", function(d) {return d.POS > x.domain()[0] && d.POS <x.domain()[1]?0:-1 })
        .attr("fill", "black");

        var variation_count_g = this.g.append("g").attr("class", "variation-count");
        var count = this.bisectVariation(this.vd, x.domain()[1]) - this.bisectVariation(this.vd, x.domain()[0]);
        variation_count_g.append("text")
        .attr("x", this.getWidth()-100)
        .attr("y", -y.bandwidth()/2 - 10)
        .attr("dy", y.bandwidth())
        .attr("fill", "orange")
        .text(count + " variations");
        
        this.renderBrush([0, this.config.brushWidth]);
    }

    renderBrush(extent) {
        var x = this.x;
        this.g.append("g")
          .attr('class', 'brush-g')
          .call(this.brush)
          .call(this.brush.move, extent)
          .selectAll(".overlay")
          .each(function(d) { d.type = "selection"; }) // Treat overlay interaction as move.
          .on("mousedown touchstart", null); // Recenter before brushing.
    }

    renderCensus(censusData) {
        this.cd = censusData;
        var census_g = this.g.append("g").attr('class', "census");
        var x = this.x;
        var y = this.y;
        var census_bands = census_g.selectAll("rect")
              .data(this.cd)
              .enter()
              .append("rect")
              .attr("class", "bar")
              .attr("x",  function(d) { return x(d["Genome Location"].split(":")[1].split("-")[0])})
              .attr("y", function(d, i) { var chrom = "chr" + d["Genome Location"].split(":")[0]; return y(chrom) + y.bandwidth()/4; })
              .attr("height", function(d, i) {return  y.bandwidth()/2; })
              .attr("width", function(d) {return x(d["Genome Location"].split(":")[1].split("-")[1]) - x(d["Genome Location"].split(":")[1].split("-")[0]);})
              .attr("fill", "cyan");
    }

    addChildLevel() {
        console.log("child level");
        var container = this.container;
        gs = new GenomeSlider(container, 1);
        gs.draw();


        /*this.gs = new GenomeSlider(this.container, this.idSuffix+1)
        if(this.idSuffix != 1) {
            this.gs.empty();
            var x = parseInt($(".selection", $(this.svgSelector)).attr("x"));
            var y = parseInt($(".selection", $(this.svgSelector)).attr("width"));
            this.gs.setXDomain([x, x+y].map(this.x.invert, this.x));
            this.gs.setYDomain(this.y.domain());
            this.gs.renderCytoBand(this.cbd);
            this.gs.renderVariations(this.vd);
            this.gs.renderCensus(this.cd);
        }*/
    }

    brushed(self) {
        if (this.gs) {
            this.gs.empty();
            this.gs.setXDomain(d3.event.selection.map(this.x.invert, this.x));
            this.gs.setYDomain(this.y.domain());
            this.gs.renderCytoBand(this.cbd);
            this.gs.renderVariations(this.vd);
            this.gs.renderCensus(this.cd);
            //this.gs.renderPQBand(this.pqd);
        } else {
            var selection = d3.event.selection.map(this.x.invert, this.x)
            var tableData = this.vd.slice(this.bisectVariation(this.vd, selection[0]), this.bisectVariation(this.vd, selection[1]));
            //$(".variation-table").bootstrapTable('load', tableData);
        }
    }
        
    getWidth() {
           return container.width() - this.config.margin.left - this.config.margin.right - this.config.extraPaddingRight;
    }

    getHeight() {
           return 80;//container.height() - this.config.margin.top - this.config.margin.bottom;
    }
}

class Layer {
    constructor(gs, index, chrom, fn) {
        this.gs = gs;
        this.index = index;
        this.chrom = chrom;
        this.fn = fn;
    }
    
    setNextLayer(layer) {
        this.nextlayer = layer;
    }
    
    render() {
        this.fn(this, gs);
    }


}

function pqlayerfn(self, gs) {
        var self = this;
        let pqArmDataPromise = new Promise(function(resolve, reject) {
                        var pqDataUrl = "/getPQArmData/" + self.chrom;
                        d3.json(pqDataUrl, function(error, data) {
                            if (error) {
                                reject("Can't load data from " + pqDataUrl);
                                return;
                            }
                            resolve(data);
                        });
                    });

        pqArmDataPromise.then(
            result => {
                console.log(gs);
                gs.setXDomain([0, d3.max(result, function(d) { return d.chromEnd_y; })]);
                gs.setYDomain(result.map(function(d) { return d.chrom; }));
                this.pqd = result;
        var p_arm_g = gs.g.append("g").attr('class', "p-arm");
        var q_arm_g = gs.g.append("g").attr('class', "q-arm");  
        var x = gs.x;
        var y = gs.y; 

        var p_arms = p_arm_g.selectAll("line")
            .data(result)
            .enter()
            .append("line")
            .attr("class", "bar")
            .attr("x1", y.bandwidth()/2)
            .attr("y1", function(d, i) {return y(d.chrom) + y.bandwidth()/2; })
            .attr("y2", function(d, i) {return y(d.chrom) + y.bandwidth()/2; })
            .attr("x2", 0)
            .style("stroke-width", y.bandwidth())
            .attr("stroke-linecap", "round")
            .attr("stroke", "#00bcd6");


        p_arms
        //.transition()
          //  .ease(d3.easeLinear)
           // .duration(function(d){return x(d.chromEnd_x)})
            .attr("x2", function(d) {return x(d.chromEnd_x) - y.bandwidth()/2});

        var q_arms = q_arm_g.selectAll("line")
            .data(result)
            .enter()
            .append("line")
            .attr("class", "bar")
            .attr("x1",  function(d) {return x(d.chromEnd_x) + y.bandwidth()/2})
            .attr("y1", function(d, i) {return y(d.chrom) + y.bandwidth()/2; })
            .attr("y2", function(d, i) {return y(d.chrom) + y.bandwidth()/2; })
            .attr("x2", function(d) {return x(d.chromEnd_x) - y.bandwidth()/2})
            .style("stroke-width", y.bandwidth())
            .attr("stroke-linecap", "round")
            .attr("stroke", "#3f4eb8");

        q_arms
        //.transition()
          //  .ease(d3.easeLinear)
            //.duration(function(d){return x(d.chromEnd_y)})
            .attr("x2", function(d) {return x(d.chromEnd_y) - y.bandwidth()/2});
                this.nextlayer.render();
               },
            error => alert(error)
        );
}

function cytobandlayerfn(self, gs) {
        var self = this;
        let cytoBandDataPromise = new Promise(function(resolve, reject) {
                        var cytoBandDataUrl = "/getCytoBand/"+ self.chrom;
                        d3.json(cytoBandDataUrl, function(error, data) {
                            if (error) {
                                reject("Can't load data from " + cytoBandDataUrl);
                                return;
                            }
                            resolve(data);
                        });
                    });

        cytoBandDataPromise.then(
            result => {
                       console.log(result);
                        gs.renderCytoBand(result);
                        this.nextlayer.render();
                       },
            error => alert(error)
        );
}

function variationlayerfn(self, gs) {
        let variationDataPromise = new Promise(function(resolve, reject) {
                        var variationDataUrl = "/getVariationAllDetails/2/"+ self.chrom;
                        d3.json(variationDataUrl, function(error, variationData) {
                            if (error) {
                                reject("Can't load data from " + variationDataUrl);
                                return;
                            }
                            resolve(variationData);
                        });
                    });

        variationDataPromise.then(
            result => {gs.renderVariations(result);},
            error => alert(error)
        );
}
