extends Node

var rows: int = 40
var columns: int = 40
var row: int = 0
var column: int = 0
var inside: bool = false

var cell_width: int = 20
var cell_height: int = 30

var RowIndicator: Label = null
var ColumnIndicator: Label = null

var preview_mark: Node2D = null

var group_moving_active: bool = false

var UI_visibility:bool = true
var night_mode: bool = true

var load_path: String = ""

var saved_scene :Node

var row_tracker := false
var row_tracker_row := 0

signal mark_changed
