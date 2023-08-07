var baseWigets = require("./base.js");
var Konva = require("konva");

var MazeModel = baseWigets.BaseModel.extend({
	defaults: _.extend(baseWigets.BaseModel.defaults, {
		_model_name: "MazeModel",
		_view_name: "MazeView",
	}),
});

const create_walls = function (layer, walls, left, bottom, ts) {
	const cr2xy = function (col, row) {
		return [left + ts * col, bottom - ts * row];
	};
	walls.map(function ([col, row]) {
		let points = [];
		if (col % 2 == 0) {
			points = [...cr2xy(col, row - 1), ...cr2xy(col, row + 1)];
		} else {
			points = [...cr2xy(col - 1, row), ...cr2xy(col + 1, row)];
		}
		let w = new Konva.Line({
			stroke: "darkred",
			strokeWidth: 10,
			closed: true,
			points: points,
		});
		layer.add(w);
	});
};

const create_av = function (layer, av, ts, l, b, t) {
	for (let i = 0; i < av; i++) {
		let x = l + ts * (2 * i + 1);
		console.log(x);
		let line = new Konva.Line({
			stroke: "gray",
			points: [x, t, x, b],
		});

		let count = new Konva.Text({
			text: i + 1,
			x: x - 2,
			y: b + ts - 10,
		});
		layer.add(line);
		layer.add(count);
	}
};

const create_st = function (layer, st, ts, l, b, r) {
	for (let i = 0; i < st; i++) {
		let y = b - ts * (2 * i + 1);

		let line = new Konva.Line({
			stroke: "gray",
			points: [l, y, r, y],
		});

		let count = new Konva.Text({
			text: i + 1,
			y: y - 2,
			x: l - ts + 5,
		});
		layer.add(line);
		layer.add(count);
	}
};

class Robot {
	constructor(obj) {
		Object.assign(this, obj);
		this.points = [];
		this.trace_enabled = true;
		this.pending_moves = [];
		this.delay = 0.2;
		let that = this;
		new Konva.Image.fromURL(this.src, function (darthNode) {
			that.set_node(darthNode);
			darthNode.setAttrs({
				x: 100,
				y: 100,
			});
			that.layer.add(darthNode);
			that.layer.batchDraw();
		});
	}

	set_node(node) {
		this.node = node;
		while (this.pending_moves.length > 0) {
			let [x, y] = this.pending_moves.shift();
			console.log(
				"🚀 ~ file: maze.js ~ line 92 ~ Robot ~ set_node ~ this.pending_moves",
				this.pending_moves,
				x,
				y
			);
			this.move_to(x, y);
		}
	}

	add_point(x, y) {
		this.points.concat([x, y]);
		console.log(this.points);
	}

	move_to(x, y) {
		if (!!!this.node) {
			this.pending_moves.push([x, y]);
			return;
		}
		let that = this;
		var anim = new Konva.Animation(function (frame) {
			that.node.x(x);
			that.node.y(y);
		}, this.layer);

		anim.start();

		let updated = this.node.position();
		if (updated.x === x && updated.y === y) {
			anim.stop();
		}
	}
}

var MazeView = baseWigets.BaseView.extend({
	// Defines how the widget gets rendered into the DOM
	render: function () {
		this.init();
		this._elem = document.createElement("div");
		this._elem.id = "container";
		this.el.append(this._elem);
		this.robots = [];
	},

	add_robot: function (robot_index, src, avenue, street, orientation, beepers) {
		this.robots[robot_index] = new Robot({
			layer,
			avenue,
			street,
			orientation,
			beepers,
			src,
		});
	},

	move_to: function (robot_index, x, y) {
		let robot = this.robots[robot_index];
		robot.move_to(x, y);
	},

	add_point: function (robot_index, x, y) {
		let robot = this.robots[robot_index];
		robot.add_point(x, y);
	},

	remove_trace: function (robot_index) {
		let robot = this.robots[robot_index];
		robot.trace_enabled = false;
		robot.clear_trace();
	},

	set_pause: function (robot_index, delay) {
		let robot = this.robots[robot_index];
		robot.delay = delay;
	},

	set_trace: function (robot_index, x, y, color = "blue") {
		let robot = this.robots[robot_index];
		robot.trace_enabled = true;
		robot.traceColor = color;
		robot.add_point(x, y);
	},

	draw_grid: function (width, height, av, st, ts, walls, beepers) {
		return new Promise(function (resolve, reject) {
			this.stage = new Konva.Stage({
				container: "container",
				width: width,
				height: height,
			});
			console.log(this.stage);

			// add canvas element
			this.layer = new Konva.Layer();
			this.stage.add(layer);

			//init
			this.ts = ts;
			let left = 2 * ts;
			let right = left + 2 * ts * av;
			let bottom = height - 2 * ts;
			let top = bottom - 2 * ts * st;

			// create avenues
			create_av(layer, av, ts, left, bottom, top);

			//create streets
			create_st(layer, st, ts, left, bottom, right);

			//border
			let line = new Konva.Line({
				stroke: "darkred",
				points: [left, bottom, right, bottom, right, top, left, top],
				strokeWidth: 10,
				closed: true,
			});
			layer.add(line);

			//create walls
			create_walls(layer, walls, left, bottom, ts);

			layer.draw();
			resolve("done drawing");
		});
	},
});

module.exports = {
	MazeModel: MazeModel,
	MazeView: MazeView,
};
