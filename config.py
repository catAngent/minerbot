from constants import *

debug = False

default_language = "en"

inventory_size = 32
inventory_page_size = 20
deleted_items = [6]
settings_size = 1
default_settings = [false]

inventory_icons = [
    "<:cobblestone:1000359792788902002>",
    "<:planks:1000395246582120498>",
    "<:stick:1000395353926938685>",
    "<:wood:1000395052293570570>",
    "<:wooden_pickaxe:1000397282300133397>",
    "<:coal:1001882247563067483>",
    "<:charcoal:1001882344896069753>",
    "<:raw_iron:1001883228417822800>",
    "<:iron:1001882630414925825>",
    "<:raw_copper:1001883339000643664>",
    "<:copper:1001883392494813214>",
    "<:raw_gold:1001893626760138932>",
    "<:gold:1001893685945970799>",
    "<:redstone:1001883514255441980>",
    "<:lapis:1001883441320693882>",
    "<:diamond:1001883546329284698>",
    "<:emerald:1001883581347536966>",
    "<:stone_pickaxe:1001900204552896723>",
    "<:iron_pickaxe:1001899995546525808>",
    "<:golden_pickaxe:1001900053373386832>",
    "<:diamond_pickaxe:1001900124248748102>",
    "<:wooden_axe:1001902648183763025>",
    "<:stone_axe:1001902864286883861>",
    "<:iron_axe:1001902919500697661>",
    "<:golden_axe:1001902735563685958>",
    "<:diamond_axe:1001902779054444604>",
    "<:wooden_shovel:1001903409726750782>",
    "<:stone_shovel:1001903472750379121>",
    "<:iron_shovel:1001903538928095232>",
    "<:golden_shovel:1001903305502511165>",
    "<:diamond_shovel:1001903352810053652>",
    "<:furnace:1001919819379130420>",
]

crafting_recipes = [
    {"name": "crafting.mine_wood_1", "time": 6, "ingredients": [], "results": [(WOOD, 1)]},
    {"name": "crafting.mine_wood_2", "time": 100, "ingredients": [(WOODEN_AXE, 1)], "results": [(WOOD, 50)]},
    {"name": "crafting.mine_wood_3", "time": 150, "ingredients": [(STONE_AXE, 1)], "results": [(WOOD, 100)]},
    {"name": "crafting.mine_wood_4", "time": 200, "ingredients": [(IRON_AXE, 1)], "results": [(WOOD, 200)]},
    {"name": "crafting.mine_wood_5", "time": 5, "ingredients": [(GOLD_AXE, 1)], "results": [(WOOD, 25)]},
    {"name": "crafting.mine_wood_6", "time": 500, "ingredients": [(DIAMOND_AXE, 1)], "results": [(WOOD, 1000)]},

    {"name": "crafting.mine_cobblestone_1", "time": 100, "ingredients": [(WOODEN_PICKAXE, 1)], "results": [(COBBLESTONE, 45), (COAL, 5)]},
    {"name": "crafting.mine_cobblestone_2", "time": 150, "ingredients": [(STONE_PICKAXE, 1)], "results": [(COBBLESTONE, 90), (COAL, 5), (RAW_IRON, 10)]},
    {"name": "crafting.mine_cobblestone_3", "time": 200, "ingredients": [(IRON_PICKAXE, 1)], "results": [(COBBLESTONE, 160), (COAL, 5), (RAW_IRON, 15), (RAW_GOLD, 18), (DIAMOND, 2)]},
    {"name": "crafting.mine_cobblestone_4", "time": 5, "ingredients": [(GOLD_PICKAXE, 1)], "results": [(COBBLESTONE, 25)]},
    {"name": "crafting.mine_cobblestone_5", "time": 500, "ingredients": [(DIAMOND_PICKAXE, 1)], "results": [(COBBLESTONE, 840), (COAL, 30), (RAW_IRON, 50), (RAW_GOLD, 70), (DIAMOND, 10)]},

    {"name": "crafting.mine_mountains_1", "time": 500, "ingredients": [(IRON_PICKAXE, 1), (IRON_SHOVEL, 1)], "results": [(COAL, 100), (RAW_COPPER, 50), (EMERALD, 5)]},
    {"name": "crafting.mine_mountains_2", "time": 500, "ingredients": [(DIAMOND_PICKAXE, 1), (DIAMOND_SHOVEL, 1)], "results": [(COAL, 200), (RAW_COPPER, 100), (EMERALD, 20)]},

    {"name": "crafting.craft_planks_1", "time": 1, "ingredients": [(WOOD, 1)], "results": [(PLANKS, 4)]},
    {"name": "crafting.craft_sticks_1", "time": 1, "ingredients": [(PLANKS, 2)], "results": [(STICK, 4)]},

    {"name": "crafting.craft_pickaxe_1", "time": 1, "ingredients": [(PLANKS, 3), (STICK, 2)], "results": [(WOODEN_PICKAXE, 1)]},
    {"name": "crafting.craft_pickaxe_2", "time": 1, "ingredients": [(COBBLESTONE, 3), (STICK, 2)], "results": [(STONE_PICKAXE, 1)]},
    {"name": "crafting.craft_pickaxe_3", "time": 1, "ingredients": [(IRON, 3), (STICK, 2)], "results": [(IRON_PICKAXE, 1)]},
    {"name": "crafting.craft_pickaxe_4", "time": 1, "ingredients": [(GOLD, 3), (STICK, 2)], "results": [(GOLD_PICKAXE, 1)]},
    {"name": "crafting.craft_pickaxe_5", "time": 1, "ingredients": [(DIAMOND, 3), (STICK, 2)], "results": [(DIAMOND_PICKAXE, 1)]},

    {"name": "crafting.craft_axe_1", "time": 1, "ingredients": [(PLANKS, 3), (STICK, 2)], "results": [(WOODEN_AXE, 1)]},
    {"name": "crafting.craft_axe_2", "time": 1, "ingredients": [(COBBLESTONE, 3), (STICK, 2)], "results": [(STONE_AXE, 1)]},
    {"name": "crafting.craft_axe_3", "time": 1, "ingredients": [(IRON, 3), (STICK, 2)], "results": [(IRON_AXE, 1)]},
    {"name": "crafting.craft_axe_4", "time": 1, "ingredients": [(GOLD, 3), (STICK, 2)], "results": [(GOLD_AXE, 1)]},
    {"name": "crafting.craft_axe_5", "time": 1, "ingredients": [(DIAMOND, 3), (STICK, 2)], "results": [(DIAMOND_AXE, 1)]},

    {"name": "crafting.craft_shovel_1", "time": 1, "ingredients": [(PLANKS, 1), (STICK, 2)], "results": [(WOODEN_SHOVEL, 1)]},
    {"name": "crafting.craft_shovel_2", "time": 1, "ingredients": [(COBBLESTONE, 1), (STICK, 2)], "results": [(STONE_SHOVEL, 1)]},
    {"name": "crafting.craft_shovel_3", "time": 1, "ingredients": [(IRON, 1), (STICK, 2)], "results": [(IRON_SHOVEL, 1)]},
    {"name": "crafting.craft_shovel_4", "time": 1, "ingredients": [(GOLD, 1), (STICK, 2)], "results": [(GOLD_SHOVEL, 1)]},
    {"name": "crafting.craft_shovel_5", "time": 1, "ingredients": [(DIAMOND, 1), (STICK, 2)], "results": [(DIAMOND_SHOVEL, 1)]},

    {"name": "crafting.build_furnace", "time": 1, "ingredients": [(COBBLESTONE, 8)], "results": [(FURNACE, 1)]},

    {"name": "crafting.smelt_wood", "time": 80, "ingredients": [(WOOD, 8), (COAL, 1), (FURNACE, 1)], "results": [(COAL, 8), (FURNACE, 1)]},
    {"name": "crafting.smelt_iron", "time": 80, "ingredients": [(RAW_IRON, 8), (COAL, 1), (FURNACE, 1)], "results": [(IRON, 8), (FURNACE, 1)]},
    {"name": "crafting.smelt_copper", "time": 80, "ingredients": [(RAW_COPPER, 8), (COAL, 1), (FURNACE, 1)], "results": [(COPPER, 8), (FURNACE, 1)]},
    {"name": "crafting.smelt_gold", "time": 80, "ingredients": [(RAW_GOLD, 8), (COAL, 1), (FURNACE, 1)], "results": [(GOLD, 8), (FURNACE, 1)]},
]

item_categories = {
    "resources": {
        "fuels": [COAL],
        "gems": [EMERALD, DIAMOND, LAPIS],
        "ingots": [IRON, COPPER, GOLD],
        "dusts": [REDSTONE],
        "ores": [RAW_COPPER, RAW_IRON, RAW_GOLD],
        "wood": [WOOD, PLANKS, STICK],
        "stones": [COBBLESTONE],
    },
    "tools": {
        "pickaxes": [WOODEN_PICKAXE, STONE_PICKAXE, IRON_PICKAXE, GOLD_PICKAXE, DIAMOND_PICKAXE],
        "axes": [WOODEN_AXE, STONE_AXE, IRON_AXE, GOLD_AXE, DIAMOND_AXE],
        "shovels": [WOODEN_SHOVEL, STONE_SHOVEL, IRON_SHOVEL, GOLD_SHOVEL, DIAMOND_SHOVEL],
    },
    "buildings": [FURNACE],
}
