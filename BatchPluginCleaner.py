# Original plugin created for Skyrim by bluebuiy
# Original Mod Page: https://www.nexusmods.com/skyrimspecialedition/mods/59598
# This ver Mod Page: https://www.nexusmods.com/fallout4/mods/84962
# Modified for Fallout 4
# For mo 2.5.2+. Use at your own risk.

import os
import operator
import re
import typing
import datetime

import mobase  # type: ignore
from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QCheckBox, QDialog, QHBoxLayout, QListView, QMessageBox, QPushButton, QVBoxLayout, QWidget

launchOptions = [
	"-IKnowWhatImDoing",
	"-QuickAutoClean",
	"-autoexit",
	"-autoload",
]


class GameInfo(typing.TypedDict):
	xEditName: str
	xEditSwitch: str
	mainMasters: set[str]
	bethPlugins: set[str]


gameInfo: dict[str, GameInfo] = {
	"Oblivion": {
		"xEditName": "TES4Edit",
		"xEditSwitch": "-tes4",
		"mainMasters": {"Oblivion.esm"},
		"bethPlugins": {
			"Update.esm",
			"DLCBattlehornCastle.esp",
			"DLCFrostcrag.esp",
			"DLCHorseArmor.esp",
			"DLCMehrunesRazor.esp",
			"DLCOrrery.esp",
			"DLCShiveringIsles.esp",
			"DLCSpellTomes.esp",
			"DLCThievesDen.esp",
			"DLCVileLair.esp",
			"Knights.esp",
		},
	},
	"Nehrim": {
		"xEditName": "TES4Edit",
		"xEditSwitch": "-tes4",
		"mainMasters": {
			"Nehrim.esm",
			"Translation.esp",
		},
		"bethPlugins": set(),
	},
	"Fallout3": {
		"xEditName": "FO3Edit",
		"xEditSwitch": "-fo3",
		"mainMasters": {"Fallout3.esm"},
		"bethPlugins": {
			"Anchorage.esm",
			"BrokenSteel.esm",
			"PointLookout.esm",
			"ThePitt.esm",
			"Zeta.esm",
		},
	},
	"FalloutNV": {
		"xEditName": "FNVEdit",
		"xEditSwitch": "-fnv",
		"mainMasters": {"FalloutNV.esm"},
		"bethPlugins": {
			"CaravanPack.esm",
			"ClassicPack.esm",
			"DeadMoney.esm",
			"GunRunnersArsenal.esm",
			"HonestHearts.esm",
			"LonesomeRoad.esm",
			"MercenaryPack.esm",
			"OldWorldBlues.esm",
			"TribalPack.esm",
		},
	},
	"TTW": {
		"xEditName": "FNVEdit",
		"xEditSwitch": "-fnv",
		"mainMasters": {
			"Fallout3.esm",
			"FalloutNV.esm",
			"TaleofTwoWastelands.esm",
			"YUPTTW.esm",
		},
		"bethPlugins": {
			"Anchorage.esm",
			"BrokenSteel.esm",
			"ThePitt.esm",
			"PointLookout.esm",
			"Zeta.esm",
			"CaravanPack.esm",
			"ClassicPack.esm",
			"DeadMoney.esm",
			"GunRunnersArsenal.esm",
			"HonestHearts.esm",
			"LonesomeRoad.esm",
			"MercenaryPack.esm",
			"OldWorldBlues.esm",
			"TribalPack.esm",
		},
	},
	"Skyrim": {
		"xEditName": "TES5Edit",
		"xEditSwitch": "-tes5",
		"mainMasters": {"Skyrim.esm"},
		"bethPlugins": {
			"Update.esm",
			"Dawnguard.esm",
			"HearthFires.esm",
			"Dragonborn.esm",
			"HighResTexturePack01.esp",
			"HighResTexturePack02.esp",
			"HighResTexturePack03.esp",
		},
	},
	"SkyrimSE": {
		"xEditName": "SSEEdit",
		"xEditSwitch": "-sse",
		"mainMasters": {"Skyrim.esm"},
		"bethPlugins": {
			"Update.esm",
			"Dawnguard.esm",
			"HearthFires.esm",
			"Dragonborn.esm",
		},
	},
	"SkyrimVR": {
		"xEditName": "TES5VREdit",
		"xEditSwitch": "-tes5vr",
		"mainMasters": {
			"Skyrim.esm",
			"SkyrimVR.esm",
		},
		"bethPlugins": {
			"Update.esm",
			"Dawnguard.esm",
			"HearthFires.esm",
			"Dragonborn.esm",
		},
	},
	"Enderal": {
		"xEditName": "EnderalEdit",
		"xEditSwitch": "-enderal",
		"mainMasters": {
			"Skyrim.esm",
			"Enderal - Forgotten Stories.esm",
		},
		"bethPlugins": {"Update.esm"},
	},
	"EnderalSE": {
		"xEditName": "EnderalSEEdit",
		"xEditSwitch": "-enderalse",
		"mainMasters": {
			"Skyrim.esm",
			"Enderal - Forgotten Stories.esm",
			"SkyUI_SE.esp",
		},
		"bethPlugins": {
			"Update.esm",
			"Dawnguard.esm",
			"HearthFires.esm",
			"Dragonborn.esm",
		},
	},
	"Fallout4": {
		"xEditName": "FO4Edit",
		"xEditSwitch": "-fo4",
		"mainMasters": {"Fallout4.esm"},
		"bethPlugins": {
			"DLCRobot.esm",
			"DLCworkshop01.esm",
			"DLCworkshop02.esm",
			"DLCworkshop03.esm",
			"DLCCoast.esm",
			"DLCNukaWorld.esm",
			"DLCUltraHighResolution.esm",
		},
	},
	"Fallout4VR": {
		"xEditName": "FO4VREdit",
		"xEditSwitch": "-fo4vr",
		"mainMasters": {
			"Fallout4.esm",
			"Fallout4_VR.esm",
		},
		"bethPlugins": {
			"DLCRobot.esm",
			"DLCworkshop01.esm",
			"DLCworkshop02.esm",
			"DLCworkshop03.esm",
			"DLCCoast.esm",
			"DLCNukaWorld.esm",
			"DLCUltraHighResolution.esm",
		},
	},
	"Fallout76": {
		"xEditName": "FO76Edit",
		"xEditSwitch": "-fo76",
		"mainMasters": {"SeventySix.esm"},
		"bethPlugins": {"NW.esm"},
	},
	"Starfield": {
		"xEditName": "SF1Edit",
		"xEditSwitch": "-sf1",
		"mainMasters": {"Starfield.esm"},
		"bethPlugins": {
			"Constellation.esm",
			"BlueprintShips-Starfield.esm",
			"OldMars.esm",
			"SFBGS003.esm",
			"SFBGS006.esm",
			"SFBGS007.esm",
			"SFBGS008.esm",
		},
	},
}

ccPattern = re.compile(r"cc\w{6}[0-9]{3}-")


class PluginSelectionLine(QWidget):
	enableChange = pyqtSignal(bool, str)

	def __init__(self, pluginName: str, parent: QWidget | None = None) -> None:
		super().__init__(parent)
		self.__pluginName = pluginName
		self.__checkbox = QCheckBox(pluginName, self)
		self.__checkbox.stateChanged.connect(self.__checkboxChange)

		layout = QVBoxLayout(self)
		layout.addWidget(self.__checkbox)

	def __checkboxChange(self, state: Qt.CheckState) -> None:  # noqa: ARG002
		self.enableChange.emit(self.__checkbox.isChecked(), self.__pluginName)

	def setState(self, state: bool) -> None:
		if state:
			self.__checkbox.setCheckState(2)  # type: ignore
		else:
			self.__checkbox.setCheckState(0)  # type: ignore


class PluginListModel(QAbstractItemModel):
	def __init__(self, parent: QWidget | None = None) -> None:
		super().__init__(parent)
		self.__data: list[tuple[bool, str, int]] = []

	def flags(self, index: QModelIndex) -> Qt.ItemFlag:
		if index.isValid():
			return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable
		return None  # type: ignore

	def index(self, row: int, column: int, parent: QModelIndex | None = None) -> QModelIndex:  # noqa: ARG002
		if column == 0:
			return self.createIndex(row, column, self.__data[row][1])
		return QModelIndex()

	def parent(self, child: QModelIndex) -> QModelIndex | None:  # type: ignore  # noqa: ARG002
		return QModelIndex()

	def rowCount(self, parent: QModelIndex | None = None) -> int:  # noqa: ARG002
		return len(self.__data)

	def columnCount(self, parent: QModelIndex | None = None) -> int:  # noqa: ARG002
		return 1

	def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.EditRole) -> Qt.CheckState | str | None:
		row = index.row()
		if role == Qt.ItemDataRole.CheckStateRole:
			if self.__data[row][0]:
				return Qt.CheckState.Checked
			return Qt.CheckState.Unchecked

		if role in {Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole}:
			return self.__data[row][1]
		return None

	def setData(self, index: QModelIndex, value: typing.Any, role: int = Qt.ItemDataRole.CheckStateRole) -> bool:
		if role == Qt.ItemDataRole.CheckStateRole and index.isValid():
			inState = None
			# Comment from bluebuiy:
			# I have no idea how these are supposed to be referenced. Qt.CheckState.Checked and Qt.CheckState.Unchecked are not working.
			if value == 2:
				inState = True
			elif value == 0:
				inState = False

			if inState is not None:
				self.__data[index.row()] = (inState, self.__data[index.row()][1], self.__data[index.row()][2])
				self.dataChanged.emit(index, index, [role])

			return True
		return False

	def addPlugin(self, pluginName: str, priority: int, state: bool) -> None:
		self.__data.append((state, pluginName, priority))

	def getEnabledPlugins(self) -> set[str]:
		ret = set()
		for item in self.__data:
			if item[0]:
				ret.add(item[1])
		return ret

	def deselectAll(self) -> None:
		self.beginResetModel()
		for i, val in enumerate(self.__data):
			self.__data[i] = (False, val[1], val[2])
		self.endResetModel()

	def selectAll(self) -> None:
		self.beginResetModel()
		for i, val in enumerate(self.__data):
			self.__data[i] = (True, val[1], val[2])
		self.endResetModel()

	def sortData(self, key: typing.Callable) -> None:
		self.beginResetModel()
		self.__data.sort(key=key)
		self.endResetModel()


class PluginSelectWindow(QDialog):
	startAction = pyqtSignal()
	cancelAction = pyqtSignal()

	def __init__(self, parent: QWidget | None = None) -> None:
		super().__init__(parent)
		self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
		self.setWindowTitle("Batch Plugin Cleaner")
		self.resize(400, 600)
		self.__listModel = PluginListModel()
		self.__layout = QHBoxLayout()
		self.__listView = QListView()
		self.__listView.setModel(self.__listModel)

		selectAllButton = QPushButton("Select All")
		selectNoneButton = QPushButton("Select None")
		startButton = QPushButton("Clean")

		self.__layout.addWidget(self.__listView)

		buttonHolder = QWidget()
		buttonLayout = QVBoxLayout(buttonHolder)

		buttonLayout.addWidget(selectAllButton)
		buttonLayout.addWidget(selectNoneButton)
		buttonLayout.addWidget(startButton)

		self.__layout.addWidget(buttonHolder)

		self.setLayout(self.__layout)

		selectAllButton.clicked.connect(self.__selectAll)
		selectNoneButton.clicked.connect(self.__selectNone)
		startButton.clicked.connect(self.__startPressed)

	def addPlugin(self, pluginName: str, priority: int, defaultState: bool) -> None:
		self.__listModel.addPlugin(pluginName, priority, defaultState)

	def getPluginList(self) -> set[str]:
		return self.__listModel.getEnabledPlugins()

	def sortPlugins(self, key: typing.Callable) -> None:
		self.__listModel.sortData(key)

	def __startPressed(self) -> None:
		self.startAction.emit()

	def __selectNone(self) -> None:
		self.__listModel.deselectAll()

	def __selectAll(self) -> None:
		self.__listModel.selectAll()


class CleanerPlugin(mobase.IPluginTool):
	def __init__(self) -> None:
		super().__init__()
		self.__canceled = False

	def init(self, organizer: mobase.IOrganizer) -> bool:
		self.__organizer = organizer
		return True

	def name(self) -> str:
		return "Batch Plugin Cleaner"

	def author(self) -> str:
		return "bluebuiy & wxMichael"

	def displayName(self) -> str:
		return "Clean Plugins"

	def description(self) -> str:
		return f'Clean all plugins with one button. Requres {gameInfo[self.__organizer.managedGame().gameShortName()]["xEditName"]}.'

	def version(self) -> mobase.VersionInfo:
		return mobase.VersionInfo(1, 1, 0)

	def isActive(self) -> mobase.MoVariant:
		return self.__organizer.pluginSetting(self.name(), "enabled")

	def tooltip(self) -> str:
		return "Clean all plugins at once"

	def settings(self) -> list[mobase.PluginSetting]:
		return [
			mobase.PluginSetting("enabled", "Enable this plugin", True),
			mobase.PluginSetting("clean_cc", "Clean Creation Club plugins", True),
			mobase.PluginSetting("clean_beth", "Clean base game plugins", False),
			mobase.PluginSetting("clean_else", "Clean mod plugins", True),
			mobase.PluginSetting("sort_by_priority", "If plugins should be ordered by priority instead of alphabetically", True),
			mobase.PluginSetting(
				"explicit_data_path",
				"If the data directory should be explicitly provided.  May need to be enabled if you get errors from xEdit.",
				False,
			),
			mobase.PluginSetting(
				"explicit_ini_path",
				"If the ini path should be explicitly provided.  May need to be enabled if you get errors from xEdit.",
				False,
			),
			mobase.PluginSetting(
				"save_dirty_plugins",
				"Sends logs and backups of dirty plugins to BatchPluginCleanerOutput folder under MO2 base path.",
				True,
			),
			mobase.PluginSetting(
				"auto_close",
				"Auto close plugin selection window after clean.",
				True,
			),
			mobase.PluginSetting("exe_name_xedit", "Invoke xEdit as xEdit, not a game-specific name such as FO4Edit.", False),
		]

	def icon(self) -> QIcon:
		return QIcon()

	def setParentWidget(self, parent: QWidget) -> None:
		self.__parentWidget = parent

	def display(self) -> None:
		self.__dialog = PluginSelectWindow(self.__parentWidget)
		self.__dialog.startAction.connect(self.__start)

		pluginList = self.__organizer.pluginList()
		pluginNames = list(pluginList.pluginNames())
		# Exclude main masters because they should not be cleaned.
		for master in gameInfo[self.__organizer.managedGame().gameShortName()]["mainMasters"]:
			if master in pluginNames:
				pluginNames.remove(master)

		cleanCC = self.__organizer.pluginSetting(self.name(), "clean_cc")
		cleanBeth = self.__organizer.pluginSetting(self.name(), "clean_beth")
		cleanElse = self.__organizer.pluginSetting(self.name(), "clean_else")
		for plugin in pluginNames:
			pluginDefaultState = False

			if pluginList.state(plugin) == mobase.PluginState.ACTIVE:
				isCC = ccPattern.match(plugin) is not None
				isBeth = plugin in gameInfo[self.__organizer.managedGame().gameShortName()]["bethPlugins"]
				if (cleanCC and isCC) or (cleanBeth and isBeth):
					pluginDefaultState = True
				if not isBeth and not isCC and cleanElse:
					pluginDefaultState = True

			self.__dialog.addPlugin(plugin, pluginList.priority(plugin), pluginDefaultState)

		if self.__organizer.pluginSetting(self.name(), "sort_by_priority"):
			self.__dialog.sortPlugins(key=operator.itemgetter(2))
		else:
			self.__dialog.sortPlugins(key=operator.itemgetter(1))

		self.__dialog.open()

	def __start(self) -> None:
		self.runClean(self.__dialog.getPluginList())

	def runClean(self, pluginNamesSet: set[str]) -> None:
		failed: list[str] = []
		logFile = False
		if self.__organizer.pluginSetting(self.name(), "save_dirty_plugins"):
			os.makedirs(f'{self.__organizer.basePath()}/BatchPluginCleanerOutput', exist_ok=True) # create the output folder if it doesn't exist
   
		xEditExecutableName = (
			"xEdit"
			if self.__organizer.pluginSetting(self.name(), "exe_name_xedit")
			else gameInfo[self.__organizer.managedGame().gameShortName()]["xEditName"]
		)
		cleanCount = 0
		totalCount = 0
		pluginNames = list(pluginNamesSet)
		# Sort the plugins so they are cleaned by priority
		pluginNames.sort(key=lambda pluginName: 0 - self.__organizer.pluginList().priority(pluginName))
		for plugin in pluginNames:
			if self.__canceled:
				self.__canceled = False
				break

			args = list(launchOptions)

			if self.__organizer.pluginSetting(self.name(), "explicit_data_path"):
				args.append(f'-D:"{self.__organizer.managedGame().dataDirectory().absolutePath()}"')

			if self.__organizer.pluginSetting(self.name(), "explicit_ini_path"):
				args.append(
					f'-I:"{self.__organizer.managedGame().documentsDirectory().path()}/{self.__organizer.managedGame().iniFiles()[0]}"'
				)
			
			if self.__organizer.pluginSetting(self.name(), "save_dirty_plugins"):
				logFile = f'{self.__organizer.basePath()}/BatchPluginCleanerOutput/{plugin}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
				args.extend((
					f'-B:"{self.__organizer.basePath()}/BatchPluginCleanerOutput/"',
					f'-R:"{logFile}"',
				))

			args.extend((
				gameInfo[self.__organizer.managedGame().gameShortName()]["xEditSwitch"],
				f'"{plugin}"',
			))

			exe = self.__organizer.startApplication(xEditExecutableName, args)
			if exe == mobase.INVALID_HANDLE_VALUE:
				QMessageBox.critical(
					self.__parentWidget,
					"Failed to start xEdit",
					f'Make sure xEdit is registered as an executable (Ctrl+E) with the name "{xEditExecutableName}"',
				)
				return

			waitResult, exitCode = self.__organizer.waitForApplication(exe, False)
			if not waitResult:
				self.__canceled = True
			elif exitCode != 0:
				failed.append(plugin)
			else:
				totalCount += 1
				if logFile:
					if search_log_file(logFile, "    dirty:"):
						cleanCount += 1
					else:
						os.remove(logFile) # remove the log file if the plugin was already clean

		if failed:
			QMessageBox.critical(self.__parentWidget, "Failed to clean some plugins!", "\n".join(failed))
		elif cleanCount > 0:
			QMessageBox.information(self.__parentWidget, "Clean successful", f"Successfully cleaned {cleanCount} of {totalCount} plugins")
   
		if self.__organizer.pluginSetting(self.name(), "auto_close"):
			self.__dialog.close()


def createPlugin() -> mobase.IPluginTool:
	return CleanerPlugin()

def search_log_file(log_file_path: str, search_string: str) -> bool:
    with open(log_file_path, 'r') as file:
        for line in file:
            if line.startswith(search_string):
                return True
    return False