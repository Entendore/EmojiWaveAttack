#!/usr/bin/env python3
"""
Emoji Survivors v3 - 75 Enemy Types + 20 Weapons + 15 Biomes
Controls: WASD/Arrow keys to move | Auto-attacks fire automatically | Survive!
"""

import pygame
import sys
import math
import random

pygame.init()
pygame.mixer.init()

SCREEN_W, SCREEN_H = 1200, 800
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
GREEN = (60, 255, 60)
BLUE = (60, 120, 255)
YELLOW = (255, 230, 50)
PURPLE = (180, 60, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
DARK_RED = (120, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
DARK_BG = (18, 14, 28)
HUD_BG = (30, 24, 45, 200)
PINK = (255, 105, 180)
LIME = (180, 255, 60)
TEAL = (0, 200, 180)
GOLD = (255, 215, 0)
MAGENTA = (255, 0, 255)
CORAL = (255, 127, 80)
STEEL = (120, 140, 160)

# ─── BIOME DEFINITIONS ─────────────────────────────────────────────────────────
BIOMES = [
    {"name": "Graveyard",       "bg": (18, 14, 28),   "grid": (30, 25, 45),  "wave": 1},
    {"name": "Haunted Cathedral","bg": (20, 18, 32),  "grid": (35, 28, 50),  "wave": 3},
    {"name": "Dark Forest",     "bg": (10, 22, 14),   "grid": (25, 40, 25),  "wave": 5},
    {"name": "Toxic Swamp",     "bg": (14, 22, 10),   "grid": (30, 45, 20),  "wave": 8},
    {"name": "Inferno",         "bg": (28, 12, 8),    "grid": (45, 25, 20),  "wave": 10},
    {"name": "Crystal Caves",   "bg": (16, 12, 30),   "grid": (28, 20, 50),  "wave": 13},
    {"name": "Frozen Waste",    "bg": (12, 18, 30),   "grid": (25, 35, 55),  "wave": 15},
    {"name": "Shadow Realm",    "bg": (14, 10, 18),   "grid": (25, 18, 35),  "wave": 18},
    {"name": "Void Realm",      "bg": (22, 8, 28),    "grid": (40, 20, 50),  "wave": 22},
    {"name": "Volcanic Peak",   "bg": (30, 10, 5),    "grid": (50, 25, 15),  "wave": 27},
    {"name": "Blood Moon",      "bg": (28, 8, 12),    "grid": (50, 20, 25),  "wave": 32},
    {"name": "Celestial Garden", "bg": (18, 16, 32),   "grid": (35, 30, 55),  "wave": 38},
    {"name": "Chaos Dimension", "bg": (24, 10, 24),   "grid": (45, 18, 45),  "wave": 45},
    {"name": "Abyss",           "bg": (8, 4, 16),     "grid": (30, 15, 40),  "wave": 50},
    {"name": "Oblivion",        "bg": (4, 2, 8),      "grid": (20, 10, 30),  "wave": 60},
]

# ─── 50 ENEMY TYPES (organized by tier) ─────────────────────────────────────────
# behavior: "chase"(default), "sine"(weave), "charge"(rush then pause),
#            "circle"(orbit player), "teleport"(blink toward player),
#            "split"(spawn 2 small on death), "explode"(AoE on death),
#            "heal_on_hit", "slow"(slows player on hit)
# special: extra data dict for behavior params
ENEMY_TYPES = {
    # ── TIER 1: Wave 1+ (Basic Undead & Critters) ──
    "zombie":        {"emoji": "\U0001f9df", "hp": 30,  "speed": 1.2, "damage": 8,  "xp": 5,  "color": GREEN,       "tier": 1, "behavior": "chase"},
    "skeleton":      {"emoji": "\U0001f480", "hp": 20,  "speed": 2.0, "damage": 5,  "xp": 4,  "color": WHITE,       "tier": 1, "behavior": "chase"},
    "bat":           {"emoji": "\U0001f987", "hp": 15,  "speed": 2.8, "damage": 4,  "xp": 3,  "color": PURPLE,      "tier": 1, "behavior": "sine",       "special": {"amp": 40, "freq": 0.06}},
    "spider":        {"emoji": "\U0001f577", "hp": 18,  "speed": 2.5, "damage": 6,  "xp": 4,  "color": (80,80,80),  "tier": 1, "behavior": "sine",       "special": {"amp": 25, "freq": 0.1}},
    "rat":           {"emoji": "\U0001f400", "hp": 8,   "speed": 3.5, "damage": 3,  "xp": 2,  "color": (140,120,100),"tier": 1,"behavior": "sine",       "special": {"amp": 15, "freq": 0.15}},
    "snake":         {"emoji": "\U0001f40d", "hp": 16,  "speed": 2.2, "damage": 7,  "xp": 4,  "color": LIME,        "tier": 1, "behavior": "sine",       "special": {"amp": 50, "freq": 0.04}},
    "wolf":          {"emoji": "\U0001f43a", "hp": 25,  "speed": 2.6, "damage": 8,  "xp": 6,  "color": GRAY,        "tier": 1, "behavior": "charge",     "special": {"charge_speed": 6, "pause_time": 40}},
    "scorpion":      {"emoji": "\U0001f982", "hp": 22,  "speed": 1.8, "damage": 10, "xp": 5,  "color": ORANGE,      "tier": 1, "behavior": "slow"},

    # ── TIER 2: Wave 2+ (Supernatural) ──
    "ghost":         {"emoji": "\U0001f47b", "hp": 25,  "speed": 1.8, "damage": 7,  "xp": 6,  "color": (200,200,255),"tier": 2, "behavior": "teleport",   "special": {"teleport_cd": 180}},
    "slime":         {"emoji": "\U0001f7e2", "hp": 20,  "speed": 1.4, "damage": 5,  "xp": 5,  "color": GREEN,       "tier": 2, "behavior": "split",      "special": {"split_into": "slime_tiny", "split_count": 2}},
    "slime_tiny":    {"emoji": "\U0001f7e1", "hp": 8,   "speed": 2.0, "damage": 3,  "xp": 2,  "color": YELLOW,      "tier": 2, "behavior": "chase"},
    "crow":          {"emoji": "\U0001f426", "hp": 12,  "speed": 3.2, "damage": 5,  "xp": 4,  "color": (60,60,60),  "tier": 2, "behavior": "circle",     "special": {"radius": 150, "orbit_speed": 0.03}},
    "mushroom":      {"emoji": "\U0001f344", "hp": 35,  "speed": 1.0, "damage": 6,  "xp": 5,  "color": (200,50,50),"tier": 2, "behavior": "explode",    "special": {"explosion_radius": 50, "explosion_dmg_mult": 1.5}},
    "zombie_dog":    {"emoji": "\U0001f436", "hp": 28,  "speed": 3.0, "damage": 9,  "xp": 6,  "color": (100,80,60),"tier": 2, "behavior": "charge",     "special": {"charge_speed": 7, "pause_time": 30}},
    "phantom":       {"emoji": "\U0001f47e", "hp": 30,  "speed": 2.4, "damage": 8,  "xp": 7,  "color": CYAN,        "tier": 2, "behavior": "teleport",   "special": {"teleport_cd": 120}},
    # cultist removed to keep exactly 50 regular types (slime_tiny is split-spawn only)

    # ── TIER 3: Wave 4+ (Dangerous Creatures) ──
    "bear":          {"emoji": "\U0001f43b", "hp": 80,  "speed": 1.3, "damage": 18, "xp": 12, "color": (139,90,43), "tier": 3, "behavior": "charge",     "special": {"charge_speed": 5, "pause_time": 60}},
    "vampire":       {"emoji": "\U0001f9db", "hp": 45,  "speed": 2.2, "damage": 12, "xp": 12, "color": RED,         "tier": 3, "behavior": "heal_on_hit"},
    "golem":         {"emoji": "\U0001faa8", "hp": 120, "speed": 0.7, "damage": 20, "xp": 15, "color": STEEL,       "tier": 3, "behavior": "chase"},
    "werewolf":      {"emoji": "\U0001f43a", "hp": 55,  "speed": 3.0, "damage": 16, "xp": 14, "color": (100,100,100),"tier":3, "behavior": "charge",    "special": {"charge_speed": 8, "pause_time": 25}},
    "witch":         {"emoji": "\U0001f9d9", "hp": 35,  "speed": 1.5, "damage": 10, "xp": 10, "color": MAGENTA,     "tier": 3, "behavior": "teleport",   "special": {"teleport_cd": 90}},
    "ice_elemental": {"emoji": "\u2744",      "hp": 40,  "speed": 1.8, "damage": 10, "xp": 10, "color": (150,200,255),"tier":3, "behavior": "slow",      "special": {"slow_duration": 90, "slow_factor": 0.5}},
    "fire_elemental":{"emoji": "\U0001f525", "hp": 45,  "speed": 1.6, "damage": 14, "xp": 11, "color": ORANGE,      "tier": 3, "behavior": "explode",    "special": {"explosion_radius": 70, "explosion_dmg_mult": 2.0}},
    "shark":         {"emoji": "\U0001f988", "hp": 50,  "speed": 3.2, "damage": 15, "xp": 13, "color": (70,130,180),"tier": 3,"behavior": "sine",       "special": {"amp": 60, "freq": 0.03}},

    # ── TIER 4: Wave 7+ (Elites & Nightmares) ──
    "demon":         {"emoji": "\U0001f608", "hp": 80,  "speed": 1.5, "damage": 15, "xp": 15, "color": RED,         "tier": 4, "behavior": "chase"},
    "clown":         {"emoji": "\U0001f921", "hp": 50,  "speed": 2.5, "damage": 14, "xp": 14, "color": RED,         "tier": 4, "behavior": "sine",       "special": {"amp": 80, "freq": 0.05}},
    "dark_knight":   {"emoji": "\u2694",      "hp": 90,  "speed": 1.4, "damage": 18, "xp": 16, "color": (60,60,80), "tier": 4, "behavior": "charge",     "special": {"charge_speed": 6, "pause_time": 50}},
    "assassin":      {"emoji": "\U0001f5e1", "hp": 35,  "speed": 3.8, "damage": 22, "xp": 18, "color": (40,40,40), "tier": 4, "behavior": "teleport",   "special": {"teleport_cd": 70}},
    "bomber":        {"emoji": "\U0001f4a3", "hp": 25,  "speed": 2.0, "damage": 8,  "xp": 10, "color": ORANGE,      "tier": 4, "behavior": "explode",    "special": {"explosion_radius": 90, "explosion_dmg_mult": 2.5}},
    "shield_bearer": {"emoji": "\U0001f6e1", "hp": 100, "speed": 1.0, "damage": 12, "xp": 14, "color": STEEL,       "tier": 4, "behavior": "chase"},
    "archer":        {"emoji": "\U0001f3f9", "hp": 30,  "speed": 2.0, "damage": 16, "xp": 12, "color": (139,90,43), "tier": 4, "behavior": "circle",     "special": {"radius": 200, "orbit_speed": 0.02}},
    "necromancer":   {"emoji": "\U0001f5b5", "hp": 60,  "speed": 1.2, "damage": 14, "xp": 18, "color": PURPLE,      "tier": 4, "behavior": "teleport",   "special": {"teleport_cd": 100}},

    # ── TIER 5: Wave 12+ (Legendary Threats) ──
    "drake":         {"emoji": "\U0001f409", "hp": 120, "speed": 1.8, "damage": 22, "xp": 22, "color": (200,50,50),"tier": 5, "behavior": "charge",     "special": {"charge_speed": 7, "pause_time": 40}},
    "lich":          {"emoji": "\U0001f9b3", "hp": 150, "speed": 1.0, "damage": 20, "xp": 25, "color": (180,180,220),"tier":5, "behavior": "teleport",   "special": {"teleport_cd": 80}},
    "kraken_tentacle":{"emoji":"\U0001f419", "hp": 80,  "speed": 2.0, "damage": 20, "xp": 20, "color": TEAL,        "tier": 5, "behavior": "sine",       "special": {"amp": 70, "freq": 0.04}},
    "storm_elem":    {"emoji": "\u26c8",      "hp": 65,  "speed": 3.5, "damage": 18, "xp": 20, "color": CYAN,        "tier": 5, "behavior": "teleport",   "special": {"teleport_cd": 50}},
    "deathstalker":  {"emoji": "\U0001f982", "hp": 70,  "speed": 2.8, "damage": 24, "xp": 22, "color": (200,150,0),"tier":5, "behavior": "slow",       "special": {"slow_duration": 120, "slow_factor": 0.4}},
    "vortex":        {"emoji": "\U0001f300", "hp": 90,  "speed": 1.5, "damage": 16, "xp": 20, "color": PURPLE,      "tier": 5, "behavior": "circle",     "special": {"radius": 120, "orbit_speed": 0.05}},
    "behemoth":      {"emoji": "\U0001f42f", "hp": 200, "speed": 0.8, "damage": 28, "xp": 28, "color": (80,40,40), "tier": 5, "behavior": "charge",     "special": {"charge_speed": 5, "pause_time": 70}},
    "wraith":        {"emoji": "\U0001f47b", "hp": 55,  "speed": 3.0, "damage": 20, "xp": 22, "color": (150,150,255),"tier":5,"behavior": "teleport",   "special": {"teleport_cd": 40}},

    # ── TIER 6: Wave 18+ (Catastrophic) ──
    "archdevil":     {"emoji": "\U0001f479", "hp": 180, "speed": 2.0, "damage": 28, "xp": 35, "color": RED,         "tier": 6, "behavior": "charge",     "special": {"charge_speed": 8, "pause_time": 30}},
    "dragon":        {"emoji": "\U0001f409", "hp": 250, "speed": 1.2, "damage": 35, "xp": 45, "color": ORANGE,      "tier": 6, "behavior": "chase"},
    "reaper":        {"emoji": "\u2620",      "hp": 100, "speed": 2.5, "damage": 40, "xp": 40, "color": (0,0,0),    "tier": 6, "behavior": "teleport",   "special": {"teleport_cd": 30}},
    "kraken":        {"emoji": "\U0001f419", "hp": 300, "speed": 1.0, "damage": 30, "xp": 50, "color": TEAL,        "tier": 6, "behavior": "circle",     "special": {"radius": 100, "orbit_speed": 0.04}},
    "void_walker":   {"emoji": "\U0001f47e", "hp": 120, "speed": 3.5, "damage": 32, "xp": 40, "color": MAGENTA,     "tier": 6, "behavior": "teleport",   "special": {"teleport_cd": 25}},
    "titan":         {"emoji": "\U0001f3c5", "hp": 400, "speed": 0.6, "damage": 45, "xp": 55, "color": GOLD,        "tier": 6, "behavior": "chase"},
    "blood_queen":   {"emoji": "\U0001f9db", "hp": 160, "speed": 2.8, "damage": 30, "xp": 42, "color": (200,0,50), "tier": 6, "behavior": "heal_on_hit"},
    "abomination":   {"emoji": "\U0001f479", "hp": 350, "speed": 0.9, "damage": 38, "xp": 48, "color": (80,120,0), "tier": 6, "behavior": "split",      "special": {"split_into": "slime", "split_count": 3}},

    # ── TIER 7: Wave 25+ (Apocalyptic Bosses) ──
    "ogre":          {"emoji": "\U0001f479", "hp": 600, "speed": 0.8, "damage": 35, "xp": 70, "color": ORANGE,      "tier": 7, "behavior": "charge",     "special": {"charge_speed": 5, "pause_time": 50}},
    "demon_lord":    {"emoji": "\U0001f608", "hp": 800, "speed": 1.0, "damage": 45, "xp": 90, "color": RED,         "tier": 7, "behavior": "teleport",   "special": {"teleport_cd": 60}},
    "elder_dragon":  {"emoji": "\U0001f409", "hp": 1000,"speed": 0.9, "damage": 50, "xp": 100,"color": (255,100,0),"tier":7, "behavior": "chase"},
    "death_itself":  {"emoji": "\u2620",      "hp": 500, "speed": 3.0, "damage": 60, "xp": 120,"color": (30,30,30), "tier": 7, "behavior": "teleport",   "special": {"teleport_cd": 20}},

    # ── TIER 8: Wave 35+ (Cosmic Horrors) ──
    "star_spawn":    {"emoji": "\U0001f31f", "hp": 700, "speed": 1.4, "damage": 55, "xp": 130,"color": GOLD,        "tier": 8, "behavior": "teleport",   "special": {"teleport_cd": 45}},
    "cosmic_horr":   {"emoji": "\U0001f300", "hp": 550, "speed": 2.0, "damage": 50, "xp": 125,"color": MAGENTA,     "tier": 8, "behavior": "circle",     "special": {"radius": 90, "orbit_speed": 0.06}},
    "sun_serpent":   {"emoji": "\u2600",      "hp": 450, "speed": 3.2, "damage": 48, "xp": 120,"color": GOLD,        "tier": 8, "behavior": "sine",       "special": {"amp": 100, "freq": 0.02}},
    "moon_cultist":   {"emoji": "\U0001f319", "hp": 400, "speed": 2.5, "damage": 45, "xp": 115,"color": (180,180,220),"tier":8, "behavior": "charge",     "special": {"charge_speed": 9, "pause_time": 20}},
    "eclipse_wraith": {"emoji": "\U0001f31a", "hp": 350, "speed": 4.0, "damage": 52, "xp": 135,"color": (50,50,80),  "tier": 8, "behavior": "teleport",   "special": {"teleport_cd": 15}},

    # ── TIER 9: Wave 45+ (Dimensional Terrors) ──
    "time_wraith":   {"emoji": "\u23f0",      "hp": 600, "speed": 2.8, "damage": 60, "xp": 160,"color": CYAN,        "tier": 9, "behavior": "teleport",   "special": {"teleport_cd": 10}},
    "quantum_beast": {"emoji": "\U0001f52c", "hp": 500, "speed": 3.5, "damage": 55, "xp": 155,"color": (100,200,255),"tier":9, "behavior": "sine",       "special": {"amp": 120, "freq": 0.08}},
    "reality_tear":  {"emoji": "\U0001f4a5", "hp": 800, "speed": 1.8, "damage": 65, "xp": 170,"color": PINK,        "tier": 9, "behavior": "explode",    "special": {"explosion_radius": 120, "explosion_dmg_mult": 3.0}},
    "void_colossus": {"emoji": "\U0001f3af", "hp": 1200,"speed": 0.7, "damage": 70, "xp": 200,"color": (60,0,80),   "tier": 9, "behavior": "charge",     "special": {"charge_speed": 6, "pause_time": 80}},
    "dimension_lord": {"emoji": "\U0001f539", "hp": 900, "speed": 2.2, "damage": 68, "xp": 190,"color": PURPLE,      "tier": 9, "behavior": "heal_on_hit"},

    # ── TIER 10: Wave 60+ (Endgame) ──
    "omega_titan":   {"emoji": "\u2726",      "hp": 2000,"speed": 0.5, "damage": 80, "xp": 300,"color": GOLD,        "tier":10, "behavior": "chase"},
    "annihilator":   {"emoji": "\U0001f4a5", "hp": 1500,"speed": 1.5, "damage": 90, "xp": 280,"color": RED,         "tier":10, "behavior": "teleport",   "special": {"teleport_cd": 8}},
    "the_end":       {"emoji": "\u2620",      "hp": 1000,"speed": 4.5, "damage": 100,"xp": 400,"color": (10,10,10),  "tier":10, "behavior": "charge",     "special": {"charge_speed": 12, "pause_time": 10}},

    # ── EXTRA: Special mechanic enemies (mixed tiers) ──
    "mosquito":      {"emoji": "\U0001f99f", "hp": 10,  "speed": 4.0, "damage": 3,  "xp": 2,  "color": (200,100,100),"tier":1,"behavior": "sine",       "special": {"amp": 30, "freq": 0.2}},
    "flea":          {"emoji": "\U0001f41c", "hp": 5,   "speed": 5.0, "damage": 2,  "xp": 1,  "color": (160,120,80),"tier":1,"behavior": "sine",       "special": {"amp": 10, "freq": 0.3}},
    "swarm_bee":     {"emoji": "\U0001f41d", "hp": 8,   "speed": 4.2, "damage": 4,  "xp": 2,  "color": YELLOW,      "tier": 1, "behavior": "sine",       "special": {"amp": 20, "freq": 0.18}},
    "crab":          {"emoji": "\U0001f980", "hp": 35,  "speed": 1.5, "damage": 12, "xp": 7,  "color": CORAL,       "tier": 2, "behavior": "charge",     "special": {"charge_speed": 5, "pause_time": 50}},
    "piranha":       {"emoji": "\U0001f41f", "hp": 12,  "speed": 3.8, "damage": 10, "xp": 5,  "color": RED,         "tier": 2, "behavior": "sine",       "special": {"amp": 40, "freq": 0.12}},
    "mimic":         {"emoji": "\U0001f4e6", "hp": 70,  "speed": 0.0, "damage": 0,  "xp": 25, "color": GOLD,        "tier": 3, "behavior": "chase",       "special": {"mimic_radius": 80}},
    "centaur":       {"emoji": "\U0001f984", "hp": 65,  "speed": 2.8, "damage": 16, "xp": 14, "color": (160,120,60),"tier":3,"behavior": "charge",     "special": {"charge_speed": 9, "pause_time": 35}},
    "hydra":         {"emoji": "\U0001f409", "hp": 160, "speed": 1.4, "damage": 22, "xp": 24, "color": LIME,        "tier": 4, "behavior": "split",      "special": {"split_into": "slime", "split_count": 2}},
    "jester":        {"emoji": "\U0001f921", "hp": 45,  "speed": 3.0, "damage": 18, "xp": 16, "color": PINK,        "tier": 4, "behavior": "circle",     "special": {"radius": 100, "orbit_speed": 0.07}},
    "executioner":   {"emoji": "\u2694",      "hp": 70,  "speed": 3.5, "damage": 28, "xp": 20, "color": (180,0,0),   "tier": 5, "behavior": "charge",     "special": {"charge_speed": 10, "pause_time": 15}},
    "frost_giant":   {"emoji": "\u2744",      "hp": 250, "speed": 0.9, "damage": 30, "xp": 30, "color": (180,220,255),"tier":5,"behavior": "slow",       "special": {"slow_duration": 150, "slow_factor": 0.3}},
    "plague_doc":    {"emoji": "\U0001f9d1", "hp": 55,  "speed": 2.0, "damage": 14, "xp": 18, "color": (100,150,50),"tier":4,"behavior": "explode",    "special": {"explosion_radius": 70, "explosion_dmg_mult": 1.8}},
    "crystal_golem": {"emoji": "\U0001f48e", "hp": 180, "speed": 0.6, "damage": 24, "xp": 22, "color": (150,100,255),"tier":5,"behavior": "chase"},
    "shadow_clone":  {"emoji": "\u263d",      "hp": 40,  "speed": 3.2, "damage": 20, "xp": 16, "color": (80,80,120), "tier": 5, "behavior": "teleport",   "special": {"teleport_cd": 35}},
    "soul_reaver":   {"emoji": "\U0001f539", "hp": 130, "speed": 2.4, "damage": 26, "xp": 24, "color": (100,0,150), "tier": 6, "behavior": "heal_on_hit"},
    "inferno_lord":  {"emoji": "\U0001f525", "hp": 220, "speed": 1.6, "damage": 35, "xp": 38, "color": (255,150,0), "tier": 6, "behavior": "explode",    "special": {"explosion_radius": 100, "explosion_dmg_mult": 2.0}},
    "glacial_wyrm":  {"emoji": "\U0001f409", "hp": 350, "speed": 1.1, "damage": 32, "xp": 42, "color": (130,200,255),"tier":7,"behavior": "slow",       "special": {"slow_duration": 180, "slow_factor": 0.3}},
    "blood_horde":   {"emoji": "\U0001fa78", "hp": 80,  "speed": 3.4, "damage": 25, "xp": 35, "color": (200,20,40), "tier": 7, "behavior": "charge",     "special": {"charge_speed": 10, "pause_time": 12}},
}

# Boss-only types (spawned specially)
BOSS_TYPES = {
    "boss_ogre":     {"emoji": "\U0001f479", "hp": 500,  "speed": 1.0, "damage": 25, "xp": 80,  "color": ORANGE,      "tier": 3, "behavior": "charge",  "special": {"charge_speed": 5, "pause_time": 50}},
    "boss_dragon":   {"emoji": "\U0001f409", "hp": 800,  "speed": 0.9, "damage": 35, "xp": 120, "color": (255,100,0), "tier": 5, "behavior": "chase"},
    "boss_demon":    {"emoji": "\U0001f608", "hp": 1200, "speed": 1.1, "damage": 40, "xp": 150, "color": RED,         "tier": 6, "behavior": "teleport","special": {"teleport_cd": 60}},
    "boss_reaper":   {"emoji": "\u2620",      "hp": 1500, "speed": 1.3, "damage": 50, "xp": 200, "color": (20,20,20), "tier": 7, "behavior": "teleport","special": {"teleport_cd": 30}},
    "boss_abyss":    {"emoji": "\U0001f300", "hp": 2500, "speed": 0.8, "damage": 60, "xp": 300, "color": PURPLE,      "tier": 7, "behavior": "circle",  "special": {"radius": 130, "orbit_speed": 0.03}},
    "boss_cosmic":   {"emoji": "\U0001f31f", "hp": 3000, "speed": 1.2, "damage": 70, "xp": 400, "color": GOLD,        "tier": 8, "behavior": "teleport", "special": {"teleport_cd": 40}},
    "boss_dimension": {"emoji": "\U0001f539", "hp": 5000, "speed": 1.0, "damage": 85, "xp": 600, "color": MAGENTA,     "tier": 9, "behavior": "heal_on_hit"},
    "boss_omega":    {"emoji": "\u2726",      "hp": 8000, "speed": 0.7, "damage": 100,"xp": 1000,"color": WHITE,       "tier":10, "behavior": "charge",  "special": {"charge_speed": 7, "pause_time": 40}},
}

# Build tier unlock map
TIER_WAVE_UNLOCK = {1: 1, 2: 2, 3: 4, 4: 7, 5: 12, 6: 18, 7: 25, 8: 35, 9: 45, 10: 60}

def get_enemies_for_wave(wave):
    """Return list of enemy type IDs available at given wave."""
    available = []
    for eid, edata in ENEMY_TYPES.items():
        unlock = TIER_WAVE_UNLOCK.get(edata["tier"], 99)
        if wave >= unlock:
            available.append(eid)
    return available

def get_boss_for_wave(wave):
    """Return appropriate boss type for wave."""
    if wave < 5:
        return "boss_ogre"
    elif wave < 15:
        return "boss_dragon"
    elif wave < 25:
        return "boss_demon"
    elif wave < 40:
        return "boss_reaper"
    elif wave < 55:
        return "boss_abyss"
    elif wave < 70:
        return "boss_cosmic"
    elif wave < 90:
        return "boss_dimension"
    else:
        return "boss_omega"


# ─── WEAPON DEFINITIONS (expanded) ─────────────────────────────────────────────
WEAPON_DEFS = {
    "dagger": {
        "emoji": "\u2694", "name": "Throwing Dagger", "desc": "Throws daggers at nearest enemy",
        "base_damage": 12, "base_cooldown": 0.8,
        "proj_speed": 10, "proj_count": 1, "pierce": 1,
        "type": "projectile", "color": LIGHT_GRAY,
    },
    "fireball": {
        "emoji": "\U0001f525", "name": "Fireball", "desc": "Launches explosive fireballs",
        "base_damage": 25, "base_cooldown": 2.0,
        "proj_speed": 7, "proj_count": 1, "pierce": 0,
        "type": "projectile", "color": ORANGE, "aoe_radius": 60,
    },
    "lightning": {
        "emoji": "\u26a1", "name": "Lightning Ring", "desc": "Zaps enemies around you",
        "base_damage": 18, "base_cooldown": 1.5,
        "type": "aoe_ring", "color": CYAN, "aoe_radius": 150,
    },
    "holy_water": {
        "emoji": "\U0001f9ea", "name": "Holy Water", "desc": "Drops damaging puddles",
        "base_damage": 8, "base_cooldown": 3.0,
        "type": "puddle", "color": PURPLE, "aoe_radius": 80, "puddle_duration": 3.0,
    },
    "garlic": {
        "emoji": "\U0001f9c4", "name": "Garlic Aura", "desc": "Passive damage + knockback aura",
        "base_damage": 5, "base_cooldown": 1.0,
        "type": "aura", "color": (200, 200, 100), "aoe_radius": 100,
    },
    "whip": {
        "emoji": "\u3030", "name": "Energy Whip", "desc": "Whips in front of you",
        "base_damage": 20, "base_cooldown": 1.2,
        "type": "whip", "color": YELLOW, "whip_range": 120, "whip_angle": 60,
    },
    "crossbow": {
        "emoji": "\U0001f3f9", "name": "Crossbow", "desc": "Fires piercing bolts",
        "base_damage": 15, "base_cooldown": 1.0,
        "proj_speed": 12, "proj_count": 1, "pierce": 3,
        "type": "projectile", "color": (139, 90, 43),
    },
    "boomerang": {
        "emoji": "\U0001fa86", "name": "Boomerang", "desc": "Returning boomerang",
        "base_damage": 22, "base_cooldown": 2.5,
        "proj_speed": 6, "proj_count": 1, "pierce": 99,
        "type": "boomerang", "color": (160, 82, 45),
    },
    "shuriken": {
        "emoji": "\U0001f5e1", "name": "Shuriken", "desc": "Spins through enemies rapidly",
        "base_damage": 10, "base_cooldown": 0.5,
        "proj_speed": 8, "proj_count": 1, "pierce": 5,
        "type": "projectile", "color": (180, 180, 180),
    },
    "blizzard": {
        "emoji": "\u2744", "name": "Blizzard", "desc": "Ice storm that slows enemies",
        "base_damage": 14, "base_cooldown": 2.5,
        "type": "aoe_ring", "color": (150, 200, 255), "aoe_radius": 180,
        "special": "slow",
    },
    "meteor": {
        "emoji": "\u2604", "name": "Meteor Strike", "desc": "Rains meteors on random enemies",
        "base_damage": 35, "base_cooldown": 3.5,
        "type": "meteor", "color": (255, 100, 0), "aoe_radius": 80,
    },
    "aura_blade": {
        "emoji": "\u2726", "name": "Aura Blade", "desc": "Rotating blades around you",
        "base_damage": 15, "base_cooldown": 0.3,
        "type": "orbit", "color": GOLD, "orbit_radius": 80, "orbit_count": 2,
    },
    "scythe": {
        "emoji": "\u2618", "name": "Reaper Scythe", "desc": "Wide arc slash around you",
        "base_damage": 28, "base_cooldown": 1.8,
        "type": "aoe_ring", "color": (100, 0, 100), "aoe_radius": 110,
    },
    "chain_lightning": {
        "emoji": "\u26a1", "name": "Chain Lightning", "desc": "Bounces between enemies",
        "base_damage": 20, "base_cooldown": 2.0,
        "type": "chain", "color": CYAN, "chain_range": 200, "chain_count": 4,
    },
    "bible": {
        "emoji": "\U0001f4d6", "name": "Holy Bible", "desc": "Homing projectiles seek enemies",
        "base_damage": 16, "base_cooldown": 1.5,
        "proj_speed": 5, "proj_count": 2, "pierce": 1,
        "type": "homing", "color": (255, 255, 200),
    },
    "plasma_cannon": {
        "emoji": "\U0001f52b", "name": "Plasma Cannon", "desc": "Devastating piercing beam",
        "base_damage": 40, "base_cooldown": 3.0,
        "proj_speed": 15, "proj_count": 1, "pierce": 8,
        "type": "projectile", "color": (0, 255, 200),
    },
    "runetracer": {
        "emoji": "\u2728", "name": "Rune Tracer", "desc": "Fires in all 8 directions",
        "base_damage": 8, "base_cooldown": 1.0,
        "proj_speed": 9, "proj_count": 8, "pierce": 1,
        "type": "radial", "color": (200, 150, 255),
    },
    "thunder_storm": {
        "emoji": "\u26c8", "name": "Thunder Storm", "desc": "Random lightning strikes on enemies",
        "base_damage": 30, "base_cooldown": 2.0,
        "type": "meteor", "color": (100, 100, 255), "aoe_radius": 100,
    },
    "death_spiral": {
        "emoji": "\u2620", "name": "Death Spiral", "desc": "Expanding ring of doom",
        "base_damage": 22, "base_cooldown": 4.0,
        "type": "aoe_ring", "color": (100, 0, 50), "aoe_radius": 250,
    },
}
ALL_WEAPONS = list(WEAPON_DEFS.keys())


class WeaponInstance:
    def __init__(self, weapon_id, level=1):
        self.id = weapon_id
        self.defn = WEAPON_DEFS[weapon_id]
        self.level = level
        self.cooldown_timer = 0
        self._recalc()

    def _recalc(self):
        d = self.defn
        lv = self.level
        self.damage = d["base_damage"] + (lv - 1) * int(d["base_damage"] * 0.25)
        self.cooldown = max(0.1, d["base_cooldown"] * (0.85 ** (lv - 1)))
        self.proj_count = d.get("proj_count", 1) + (lv - 1) // 2
        self.pierce = d.get("pierce", 1) + (lv - 1) // 3
        self.aoe_radius = d.get("aoe_radius", 0) + (lv - 1) * 15
        self.puddle_duration = d.get("puddle_duration", 0) + (lv - 1) * 0.5
        self.whip_range = d.get("whip_range", 0) + (lv - 1) * 20
        self.orbit_count = d.get("orbit_count", 2) + (lv - 1) // 3
        self.orbit_radius = d.get("orbit_radius", 80) + (lv - 1) * 10
        self.chain_count = d.get("chain_count", 4) + (lv - 1) // 2
        self.chain_range = d.get("chain_range", 200) + (lv - 1) * 20


# ─── CAMERA ────────────────────────────────────────────────────────────────────
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
    def update(self, tx, ty):
        self.x = tx - SCREEN_W // 2
        self.y = ty - SCREEN_H // 2
    def apply(self, x, y):
        return x - self.x, y - self.y


# ─── PARTICLE ──────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color, dx=0, dy=0, life=30, size=3, text=None, font_size=16):
        self.x, self.y = float(x), float(y)
        self.color = color
        self.dx, self.dy = dx, dy
        self.life = self.max_life = life
        self.size = size
        self.text = text
        self.font = None
        if text:
            self.font = find_emoji_font(font_size)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.05
        self.life -= 1
        return self.life > 0

    def draw(self, surf, cam):
        alpha = max(0, min(255, int(255 * self.life / self.max_life)))
        sx, sy = cam.apply(self.x, self.y)
        if not (-50 < sx < SCREEN_W + 50 and -50 < sy < SCREEN_H + 50):
            return
        if self.text and self.font:
            ts = self.font.render(self.text, True, self.color)
            ts.set_alpha(alpha)
            surf.blit(ts, (sx - ts.get_width() // 2, sy - ts.get_height() // 2))
        else:
            s = max(1, int(self.size * self.life / self.max_life))
            ps = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*self.color[:3], alpha), (s, s), s)
            surf.blit(ps, (sx - s, sy - s))


# ─── FLOATING TEXT ────────────────────────────────────────────────────────────
class FloatingText:
    def __init__(self, x, y, text, color, life=25, size=16):
        self.x, self.y = float(x), float(y)
        self.text = text
        self.color = color
        self.life = self.max_life = life
        self.font = find_emoji_font(size)

    def update(self):
        self.y -= 1.2
        self.life -= 1
        return self.life > 0

    def draw(self, surf, cam):
        alpha = max(0, min(255, int(255 * self.life / self.max_life)))
        sx, sy = cam.apply(self.x, self.y)
        ts = self.font.render(self.text, True, self.color)
        ts.set_alpha(alpha)
        surf.blit(ts, (sx - ts.get_width() // 2, sy))


# ─── PROJECTILE ────────────────────────────────────────────────────────────────
class Projectile:
    def __init__(self, x, y, dx, dy, damage, weapon_inst, is_boomerang=False):
        self.x, self.y = float(x), float(y)
        self.dx, self.dy = float(dx), float(dy)
        self.damage = damage
        self.weapon = weapon_inst
        self.pierce = weapon_inst.pierce
        self.hit_enemies = set()
        self.alive = True
        self.is_boomerang = is_boomerang
        self.lifetime = 0
        self.max_lifetime = 180 if not is_boomerang else 120
        self.returning = False
        self.origin_x, self.origin_y = float(x), float(y)

    def update(self, player):
        self.lifetime += 1
        if self.is_boomerang:
            dist = math.hypot(self.x - self.origin_x, self.y - self.origin_y)
            if dist > 200 or self.lifetime > 40:
                self.returning = True
            if self.returning:
                ax = player.x - self.x
                ay = player.y - self.y
                ad = math.hypot(ax, ay) + 0.01
                self.dx = self.dx * 0.92 + (ax / ad) * 0.8
                self.dy = self.dy * 0.92 + (ay / ad) * 0.8
                if ad < 30:
                    self.alive = False
        self.x += self.dx
        self.y += self.dy
        if self.lifetime > self.max_lifetime:
            self.alive = False

    def draw(self, surf, cam):
        sx, sy = cam.apply(self.x, self.y)
        if -30 < sx < SCREEN_W + 30 and -30 < sy < SCREEN_H + 30:
            ts = emoji_font.render(self.weapon.defn["emoji"], True, WHITE)
            surf.blit(ts, (sx - ts.get_width() // 2, sy - ts.get_height() // 2))


# ─── HOMING PROJECTILE ─────────────────────────────────────────────────────────
class HomingProjectile(Projectile):
    def __init__(self, x, y, dx, dy, damage, weapon_inst, turn_speed=0.1):
        super().__init__(x, y, dx, dy, damage, weapon_inst)
        self.turn_speed = turn_speed

    def update(self, player, enemies=None):
        self.lifetime += 1
        if enemies is None:
            enemies = []
        best, best_d = None, 300
        for e in enemies:
            if not e.alive or id(e) in self.hit_enemies:
                continue
            d = math.hypot(e.x - self.x, e.y - self.y)
            if d < best_d:
                best_d, best = d, e
        if best:
            desired = math.atan2(best.y - self.y, best.x - self.x)
            current = math.atan2(self.dy, self.dx)
            diff = (desired - current + math.pi) % (2 * math.pi) - math.pi
            current += diff * self.turn_speed
            spd = math.hypot(self.dx, self.dy)
            self.dx = math.cos(current) * spd
            self.dy = math.sin(current) * spd
        self.x += self.dx
        self.y += self.dy
        if self.lifetime > self.max_lifetime:
            self.alive = False


# ─── PUDDLE ────────────────────────────────────────────────────────────────────
class Puddle:
    def __init__(self, x, y, weapon_inst):
        self.x, self.y = x, y
        self.weapon = weapon_inst
        self.duration = weapon_inst.puddle_duration
        self.timer = 0.0
        self.damage_tick = 0.0
        self.hit_set = set()
        self.alive = True
        self.radius = weapon_inst.aoe_radius

    def update(self, dt):
        self.timer += dt
        self.damage_tick += dt
        if self.damage_tick >= 0.5:
            self.damage_tick = 0
            self.hit_set.clear()
        if self.timer >= self.duration:
            self.alive = False

    def draw(self, surf, cam):
        sx, sy = cam.apply(self.x, self.y)
        alpha = max(0, min(120, int(120 * (1 - self.timer / self.duration))))
        r = self.radius
        ps = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(ps, (160, 60, 255, alpha), (r, r), r)
        pygame.draw.circle(ps, (200, 100, 255, alpha // 2), (r, r), r // 2)
        surf.blit(ps, (sx - r, sy - r))
        ts = emoji_font_sm.render(self.weapon.defn["emoji"], True, WHITE)
        surf.blit(ts, (sx - ts.get_width() // 2, sy - ts.get_height() // 2))


# ─── ENEMY (with behavior system) ──────────────────────────────────────────────
class Enemy:
    def __init__(self, x, y, etype, wave_mult=1.0, is_boss=False):
        self.x, self.y = float(x), float(y)
        self.etype = etype
        all_types = {**ENEMY_TYPES, **BOSS_TYPES}
        d = all_types.get(etype, ENEMY_TYPES["zombie"])
        self.emoji = d["emoji"]
        self.max_hp = int(d["hp"] * wave_mult)
        self.hp = self.max_hp
        self.base_speed = d["speed"] * (1 + wave_mult * 0.04)
        self.speed = self.base_speed
        self.damage = int(d["damage"] * wave_mult)
        self.xp_value = int(d["xp"] * wave_mult)
        self.color = d["color"]
        self.alive = True
        self.hit_flash = 0
        self.knockback_x = 0.0
        self.knockback_y = 0.0
        self.is_boss = is_boss
        self.size = 36 if is_boss else 20
        self.behavior = d.get("behavior", "chase")
        self.special = d.get("special", {})
        self.age = 0
        self.behavior_timer = 0
        self.behavior_phase = "active"
        self.orbit_angle = random.uniform(0, math.pi * 2)
        self.sine_offset = random.uniform(0, math.pi * 2)
        self.teleport_timer = self.special.get("teleport_cd", 120)

    def update(self, player, enemies):
        if self.hit_flash > 0:
            self.hit_flash -= 1
        self.age += 1

        ax = player.x - self.x
        ay = player.y - self.y
        dist = math.hypot(ax, ay) + 0.01
        nx, ny = ax / dist, ay / dist

        # Separation
        sep_x, sep_y = 0.0, 0.0
        for other in enemies:
            if other is self or not other.alive:
                continue
            ox = self.x - other.x
            oy = self.y - other.y
            od = math.hypot(ox, oy) + 0.01
            if od < 30:
                sep_x += ox / od * 0.5
                sep_y += oy / od * 0.5

        mx, my = 0.0, 0.0

        if self.behavior == "chase":
            mx = nx * self.speed
            my = ny * self.speed

        elif self.behavior == "sine":
            amp = self.special.get("amp", 40)
            freq = self.special.get("freq", 0.06)
            perp_x, perp_y = -ny, nx
            wave = math.sin(self.age * freq + self.sine_offset) * amp * 0.02
            mx = nx * self.speed + perp_x * wave
            my = ny * self.speed + perp_y * wave

        elif self.behavior == "charge":
            if self.behavior_phase == "active":
                self.behavior_timer += 1
                pause_max = self.special.get("pause_time", 40)
                mx = nx * self.speed * 0.3
                my = ny * self.speed * 0.3
                if self.behavior_timer > pause_max and dist < 250:
                    self.behavior_phase = "charging"
                    self.behavior_timer = 0
                    self.charge_dx = nx
                    self.charge_dy = ny
            elif self.behavior_phase == "charging":
                charge_spd = self.special.get("charge_speed", 6)
                mx = self.charge_dx * charge_spd
                my = self.charge_dy * charge_spd
                self.behavior_timer += 1
                if self.behavior_timer > 30:
                    self.behavior_phase = "cooldown"
                    self.behavior_timer = 0
            elif self.behavior_phase == "cooldown":
                mx = 0
                my = 0
                self.behavior_timer += 1
                if self.behavior_timer > 20:
                    self.behavior_phase = "active"
                    self.behavior_timer = 0

        elif self.behavior == "circle":
            radius = self.special.get("radius", 150)
            orbit_spd = self.special.get("orbit_speed", 0.03)
            self.orbit_angle += orbit_spd
            target_x = player.x + math.cos(self.orbit_angle) * radius
            target_y = player.y + math.sin(self.orbit_angle) * radius
            tx = target_x - self.x
            ty = target_y - self.y
            td = math.hypot(tx, ty) + 0.01
            spd = min(self.speed * 2, td)
            mx = (tx / td) * spd
            my = (ty / td) * spd
            # Also slowly close in
            if dist > radius * 1.2:
                mx += nx * self.speed * 0.5
                my += ny * self.speed * 0.5

        elif self.behavior == "teleport":
            mx = nx * self.speed
            my = ny * self.speed
            self.teleport_timer -= 1
            if self.teleport_timer <= 0:
                self.teleport_timer = self.special.get("teleport_cd", 120)
                # Blink closer
                if dist > 100:
                    blink_dist = min(dist - 80, 200)
                    self.x += nx * blink_dist
                    self.y += ny * blink_dist
                    for _ in range(5):
                        self._teleport_particle = True

        elif self.behavior == "slow":
            mx = nx * self.speed
            my = ny * self.speed

        elif self.behavior == "heal_on_hit":
            mx = nx * self.speed
            my = ny * self.speed

        elif self.behavior == "explode":
            mx = nx * self.speed
            my = ny * self.speed

        elif self.behavior == "split":
            mx = nx * self.speed
            my = ny * self.speed

        self.x += mx + sep_x + self.knockback_x
        self.y += my + sep_y + self.knockback_y
        self.knockback_x *= 0.8
        self.knockback_y *= 0.8

    def on_hit_player(self, player, game):
        """Called when this enemy damages the player. Returns extra spawn list."""
        spawns = []
        if self.behavior == "heal_on_hit":
            heal = max(1, self.damage // 3)
            self.hp = min(self.hp + heal, self.max_hp)
        if self.behavior == "slow":
            slow_dur = self.special.get("slow_duration", 90)
            slow_factor = self.special.get("slow_factor", 0.5)
            player.speed_mult = slow_factor
            player.speed_mult_timer = slow_dur
        return spawns

    def on_death(self, game):
        """Called when killed. Returns list of (etype, x, y) to spawn."""
        spawns = []
        if self.behavior == "split" and "split_into" in self.special:
            count = self.special.get("split_count", 2)
            for _ in range(count):
                ox = random.uniform(-20, 20)
                oy = random.uniform(-20, 20)
                spawns.append((self.special["split_into"], self.x + ox, self.y + oy))
        if self.behavior == "explode":
            radius = self.special.get("explosion_radius", 60)
            dmg_mult = self.special.get("explosion_dmg_mult", 1.5)
            exp_dmg = int(self.damage * dmg_mult)
            # Damage player if in range
            pdist = math.hypot(self.x - game.player.x, self.y - game.player.y)
            if pdist < radius:
                if game.player.take_damage(exp_dmg):
                    game.add_shake(5)
                    game.floating_texts.append(FloatingText(
                        game.player.x, game.player.y - 30,
                        str(exp_dmg), ORANGE, life=30, size=20))
            # Damage other enemies
            for e in game.enemies:
                if not e.alive or e is self:
                    continue
                if math.hypot(self.x - e.x, self.y - e.y) < radius:
                    e.take_damage(exp_dmg)
            for _ in range(20):
                a = random.uniform(0, math.pi * 2)
                r = random.uniform(0, radius)
                game.particles.append(Particle(
                    self.x + math.cos(a) * r, self.y + math.sin(a) * r,
                    ORANGE, life=20, size=5))
            game.add_shake(6)
        return spawns

    def take_damage(self, dmg, kbx=0, kby=0):
        self.hp -= dmg
        self.hit_flash = 6
        self.knockback_x += kbx
        self.knockback_y += kby
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw(self, surf, cam):
        sx, sy = cam.apply(self.x, self.y)
        if not (-50 < sx < SCREEN_W + 50 and -50 < sy < SCREEN_H + 50):
            return
        # HP bar
        if self.hp < self.max_hp:
            bw = 50 if self.is_boss else 30
            bh = 4
            bx = sx - bw // 2
            by = sy - self.size - 8
            pygame.draw.rect(surf, DARK_RED, (bx, by, bw, bh))
            hw = max(0, int(bw * self.hp / self.max_hp))
            if hw > 0:
                pygame.draw.rect(surf, RED, (bx, by, hw, bh))
        # Shadow
        shadow = pygame.Surface((self.size, self.size // 3), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), shadow.get_rect())
        surf.blit(shadow, (sx - self.size // 2, sy + self.size // 2 - 4))
        # Emoji
        ts = emoji_font.render(self.emoji, True, WHITE)
        if self.hit_flash > 0:
            surf.blit(ts, (sx - ts.get_width() // 2, sy - ts.get_height() // 2))
            fs = pygame.Surface(ts.get_size(), pygame.SRCALPHA)
            fs.fill((255, 255, 255, 100))
            surf.blit(fs, (sx - ts.get_width() // 2, sy - ts.get_height() // 2))
        else:
            surf.blit(ts, (sx - ts.get_width() // 2, sy - ts.get_height() // 2))
        # Teleport flash
        if self.behavior == "teleport" and hasattr(self, '_teleport_particle') and self._teleport_particle:
            self._teleport_particle = False
            for _ in range(3):
                game_ref = getattr(self, '_game', None)
                if game_ref:
                    game_ref.particles.append(Particle(self.x, self.y, PURPLE, life=10, size=4))
        # Boss crown
        if self.is_boss:
            ct = emoji_font_sm.render("\U0001f451", True, GOLD)
            surf.blit(ct, (sx - ct.get_width() // 2, sy - self.size - 22))


# ─── XP GEM ────────────────────────────────────────────────────────────────────
class XPGem:
    def __init__(self, x, y, value, is_cursed=False):
        self.x, self.y = float(x), float(y)
        self.value = value
        self.alive = True
        self.magnet_range = 100
        self.attracted = False
        self.bob_offset = random.uniform(0, math.pi * 2)
        self.is_cursed = is_cursed

    def update(self, player, frame):
        dist = math.hypot(player.x - self.x, player.y - self.y)
        if dist < self.magnet_range or self.attracted:
            self.attracted = True
            ax = player.x - self.x
            ay = player.y - self.y
            d = math.hypot(ax, ay) + 0.01
            speed = min(8, 200 / (d + 1))
            self.x += (ax / d) * speed
            self.y += (ay / d) * speed
        if dist < 20:
            self.alive = False
            return self.value
        return 0

    def draw(self, surf, cam, frame):
        sx, sy = cam.apply(self.x, self.y)
        bob = math.sin(frame * 0.1 + self.bob_offset) * 3
        sy += int(bob)
        if -20 < sx < SCREEN_W + 20 and -20 < sy < SCREEN_H + 20:
            emoji = "\U0001f48e" if not self.is_cursed else "\U0001f539"
            ts = emoji_font_sm.render(emoji, True, WHITE)
            surf.blit(ts, (sx - ts.get_width() // 2, sy - ts.get_height() // 2))


# ─── HEALTH PICKUP ─────────────────────────────────────────────────────────────
class HealthPickup:
    def __init__(self, x, y, heal=20):
        self.x, self.y = float(x), float(y)
        self.heal_amount = heal
        self.alive = True
        self.lifetime = 600

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, surf, cam):
        sx, sy = cam.apply(self.x, self.y)
        if -20 < sx < SCREEN_W + 20 and -20 < sy < SCREEN_H + 20:
            alpha = 255 if self.lifetime > 60 else int(255 * self.lifetime / 60)
            ts = emoji_font_sm.render("\u2764", True, WHITE)
            ts.set_alpha(alpha)
            surf.blit(ts, (sx - ts.get_width() // 2, sy - ts.get_height() // 2))


# ─── CHEST PICKUP ──────────────────────────────────────────────────────────────
class ChestPickup:
    def __init__(self, x, y, rarity="common"):
        self.x, self.y = float(x), float(y)
        self.rarity = rarity
        self.alive = True
        self.lifetime = 900
        self.opened = False
        self.open_timer = 0
        colors = {"common": YELLOW, "rare": BLUE, "epic": PURPLE, "legendary": GOLD}
        self.color = colors.get(rarity, YELLOW)
        emojis = {"common": "\U0001f4e6", "rare": "\U0001f513", "epic": "\u2728", "legendary": "\U0001f3c6"}
        self.emoji = emojis.get(rarity, "\U0001f4e6")

    def update(self):
        if not self.opened:
            self.lifetime -= 1
            if self.lifetime <= 0:
                self.alive = False
        else:
            self.open_timer += 1
            if self.open_timer > 30:
                self.alive = False

    def draw(self, surf, cam, frame):
        sx, sy = cam.apply(self.x, self.y)
        if -30 < sx < SCREEN_W + 30 and -30 < sy < SCREEN_H + 30:
            if self.opened:
                for i in range(6):
                    a = (self.open_timer * 0.2 + i * math.pi / 3)
                    r = self.open_timer * 2
                    px = sx + math.cos(a) * r
                    py = sy + math.sin(a) * r
                    alpha = max(0, 255 - self.open_timer * 8)
                    ps = pygame.Surface((6, 6), pygame.SRCALPHA)
                    pygame.draw.circle(ps, (*self.color, alpha), (3, 3), 3)
                    surf.blit(ps, (int(px) - 3, int(py) - 3))
            else:
                bob = math.sin(frame * 0.08) * 4
                ts = emoji_font.render(self.emoji, True, WHITE)
                surf.blit(ts, (sx - ts.get_width() // 2, sy + int(bob) - ts.get_height() // 2))
                # Glow
                glow = pygame.Surface((40, 40), pygame.SRCALPHA)
                pygame.draw.circle(glow, (*self.color, 40), (20, 20), 20)
                surf.blit(glow, (sx - 20, sy + int(bob) - 20))


# ─── PLAYER ────────────────────────────────────────────────────────────────────
class Player:
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.max_hp = 100
        self.hp = 100
        self.speed = 3.5
        self.speed_mult = 1.0
        self.speed_mult_timer = 0
        self.xp = 0
        self.level = 1
        self.xp_to_next = 10
        self.weapons = []
        self.armor = 0
        self.regen = 0
        self.regen_timer = 0
        self.size = 20
        self.invincible_timer = 0
        self.damage_bonus = 0
        self.crit_chance = 0.05
        self.crit_mult = 2.0
        self.luck = 0.0
        self.cdr = 0.0  # cooldown reduction
        self.pickup_range = 100
        self.move_dir = (0.0, 0.0)
        self.rerolls = 1
        self.total_xp = 0
        self.dash_cooldown = 0
        self.dash_timer = 0
        self.max_weapons = 6

    def add_weapon(self, wid):
        if len(self.weapons) < self.max_weapons:
            self.weapons.append(WeaponInstance(wid))

    def gain_xp(self, amount):
        self.xp += amount
        self.total_xp += amount
        leveled = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.3) + 5
            self.max_hp += 5
            self.hp = min(self.hp + 15, self.max_hp)
            self.crit_chance = min(0.5, self.crit_chance + 0.005)
            leveled = True
        return leveled

    def take_damage(self, dmg):
        if self.invincible_timer > 0:
            return False
        actual = max(1, dmg - self.armor)
        self.hp -= actual
        self.invincible_timer = 30
        return True

    def update(self, keys):
        dx, dy = 0.0, 0.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:   dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:   dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  dx += 1
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        effective_speed = self.speed * self.speed_mult
        if self.speed_mult_timer > 0:
            self.speed_mult_timer -= 1
            if self.speed_mult_timer <= 0:
                self.speed_mult = 1.0

        self.x += dx * effective_speed
        self.y += dy * effective_speed
        self.move_dir = (dx, dy)
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.regen > 0:
            self.regen_timer += 1
            if self.regen_timer >= 60:
                self.regen_timer = 0
                self.hp = min(self.hp + self.regen, self.max_hp)

    def draw(self, surf, cam):
        sx, sy = cam.apply(self.x, self.y)
        shadow = pygame.Surface((30, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 80), shadow.get_rect())
        surf.blit(shadow, (sx - 15, sy + 14))
        if self.invincible_timer > 0 and self.invincible_timer % 6 < 3:
            return
        ts = emoji_font_lg.render("\U0001f9d9", True, WHITE)
        surf.blit(ts, (sx - ts.get_width() // 2, sy - ts.get_height() // 2))
        # Speed debuff indicator
        if self.speed_mult < 1.0:
            st = emoji_font_sm.render("\u2744", True, CYAN)
            surf.blit(st, (sx - st.get_width() // 2, sy - 35))


# ─── MAIN GAME ─────────────────────────────────────────────────────────────────
MILESTONE_REWARDS = {
    5:  ("reroll", "Reroll +1"),
    10: ("reroll", "Reroll +1"),
    15: ("weapon_slot", "Max Weapons +1"),
    20: ("reroll", "Reroll +2"),
    25: ("heal_full", "Full Heal"),
    30: ("weapon_slot", "Max Weapons +1"),
    40: ("reroll", "Reroll +2"),
    50: ("heal_full", "Full Heal + Reroll +2"),
}

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Emoji Survivors v3 - 75 Enemies | 20 Weapons")
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        self.player = Player(0, 0)
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.xp_gems = []
        self.health_pickups = []
        self.chest_pickups = []
        self.puddles = []
        self.floating_texts = []
        self.wave = 1
        self.wave_timer = 0
        self.spawn_timer = 0
        self.game_time = 0
        self.frame = 0
        self.kill_count = 0
        self.paused = False
        self.game_over = False
        self.level_up_pending = False
        self.upgrade_choices = []
        self.screen_shake = 0
        self.shake_x = 0
        self.shake_y = 0

        self.font_lg = pygame.font.SysFont("segoeui,arial", 36, bold=True)
        self.font_md = pygame.font.SysFont("segoeui,arial", 22)
        self.font_sm = pygame.font.SysFont("segoeui,arial", 16)
        self.font_title = pygame.font.SysFont("segoeui,arial", 60, bold=True)
        self.font_xs = pygame.font.SysFont("segoeui,arial", 13)

        self.player.add_weapon("dagger")

        self.wave_duration = 30 * FPS
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_mult = 1.0
        self.max_combo = 0
        self.bestiary_seen = set()
        self.bestiary_killed = set()
        self.milestone_queue = []
        self.milestone_display_timer = 0
        self.milestone_display_text = ""
        self.total_dmg_dealt = 0
        self.biome_idx = 0
        self.biome = BIOMES[0]
        self.wave_announce_timer = 0
        self.wave_announce_text = ""
        self.new_enemy_announce_timer = 0
        self.new_enemy_announce_emoji = ""
        self.new_enemy_announce_name = ""

    # ── SPAWNING ──
    def spawn_enemy(self, force_type=None):
        angle = random.uniform(0, math.pi * 2)
        dist = random.uniform(500, 700)
        x = self.player.x + math.cos(angle) * dist
        y = self.player.y + math.sin(angle) * dist
        wave_mult = 1.0 + (self.wave - 1) * 0.12

        if force_type:
            etype = force_type
        else:
            available = get_enemies_for_wave(self.wave)
            if not available:
                available = ["zombie"]
            # Weight by tier (lower tiers more common)
            weights = []
            for e in available:
                tier = ENEMY_TYPES.get(e, {}).get("tier", 1)
                w = max(1, 6 - tier)
                weights.append(w)
            etype = random.choices(available, weights=weights, k=1)[0]

        enemy = Enemy(x, y, etype, wave_mult)
        enemy._game = self
        self.enemies.append(enemy)

        # Track bestiary
        if etype not in self.bestiary_seen:
            self.bestiary_seen.add(etype)
            d = ENEMY_TYPES.get(etype, BOSS_TYPES.get(etype, {}))
            self.new_enemy_announce_timer = 120
            self.new_enemy_announce_emoji = d.get("emoji", "?")
            self.new_enemy_announce_name = etype.replace("_", " ").title()

    def spawn_boss(self):
        boss_id = get_boss_for_wave(self.wave)
        angle = random.uniform(0, math.pi * 2)
        x = self.player.x + math.cos(angle) * 400
        y = self.player.y + math.sin(angle) * 400
        wave_mult = 1.0 + (self.wave - 1) * 0.18
        enemy = Enemy(x, y, boss_id, wave_mult, is_boss=True)
        enemy._game = self
        self.enemies.append(enemy)
        self.add_shake(10)
        self.bestiary_seen.add(boss_id)

    # ── WEAPONS ──
    def process_weapons(self):
        for weapon in self.player.weapons:
            cd = weapon.cooldown * (1.0 - self.player.cdr)
            weapon.cooldown_timer -= 1.0 / FPS
            if weapon.cooldown_timer > 0:
                continue
            weapon.cooldown_timer = cd
            wtype = weapon.defn["type"]
            total_dmg = weapon.damage + self.player.damage_bonus
            is_crit = random.random() < self.player.crit_chance
            if is_crit:
                total_dmg = int(total_dmg * self.player.crit_mult)

            if wtype == "projectile":
                nearest = self._nearest_enemy()
                if not nearest:
                    continue
                for i in range(weapon.proj_count):
                    spread = (i - (weapon.proj_count - 1) / 2) * 0.15
                    ax = nearest.x - self.player.x
                    ay = nearest.y - self.player.y
                    angle = math.atan2(ay, ax) + spread
                    spd = weapon.defn["proj_speed"]
                    self.projectiles.append(Projectile(
                        self.player.x, self.player.y,
                        math.cos(angle) * spd, math.sin(angle) * spd,
                        total_dmg, weapon))
                    if is_crit:
                        self.floating_texts.append(FloatingText(
                            self.player.x, self.player.y - 40,
                            "CRIT!", GOLD, life=20, size=14))

            elif wtype == "boomerang":
                nearest = self._nearest_enemy()
                if not nearest:
                    continue
                ax = nearest.x - self.player.x
                ay = nearest.y - self.player.y
                angle = math.atan2(ay, ax)
                spd = weapon.defn["proj_speed"]
                self.projectiles.append(Projectile(
                    self.player.x, self.player.y,
                    math.cos(angle) * spd, math.sin(angle) * spd,
                    total_dmg, weapon, is_boomerang=True))

            elif wtype == "aoe_ring":
                r = weapon.aoe_radius
                for e in self.enemies:
                    if not e.alive:
                        continue
                    if math.hypot(e.x - self.player.x, e.y - self.player.y) < r:
                        if e.take_damage(total_dmg):
                            self._on_kill(e)
                        if weapon.defn.get("special") == "slow":
                            e.speed = e.base_speed * 0.5
                            e._slow_timer = 120
                for _ in range(12):
                    a = random.uniform(0, math.pi * 2)
                    rd = random.uniform(0, r)
                    self.particles.append(Particle(
                        self.player.x + math.cos(a) * rd,
                        self.player.y + math.sin(a) * rd,
                        weapon.defn["color"], life=15, size=4))

            elif wtype == "puddle":
                self.puddles.append(Puddle(self.player.x, self.player.y, weapon))

            elif wtype == "aura":
                r = weapon.aoe_radius
                for e in self.enemies:
                    if not e.alive:
                        continue
                    d = math.hypot(e.x - self.player.x, e.y - self.player.y)
                    if d < r:
                        if e.take_damage(total_dmg):
                            self._on_kill(e)
                        if d > 0:
                            e.knockback_x += (e.x - self.player.x) / d * 2
                            e.knockback_y += (e.y - self.player.y) / d * 2
                for _ in range(3):
                    a = random.uniform(0, math.pi * 2)
                    self.particles.append(Particle(
                        self.player.x + math.cos(a) * r * 0.9,
                        self.player.y + math.sin(a) * r * 0.9,
                        weapon.defn["color"], life=10, size=3))

            elif wtype == "whip":
                fa = math.atan2(self.player.move_dir[1], self.player.move_dir[0])
                if self.player.move_dir == (0.0, 0.0):
                    fa = 0
                half = math.radians(weapon.defn.get("whip_angle", 60)) / 2
                for e in self.enemies:
                    if not e.alive:
                        continue
                    d = math.hypot(e.x - self.player.x, e.y - self.player.y)
                    if d < weapon.whip_range:
                        ea = math.atan2(e.y - self.player.y, e.x - self.player.x)
                        diff = abs((ea - fa + math.pi) % (2 * math.pi) - math.pi)
                        if diff < half:
                            if e.take_damage(total_dmg):
                                self._on_kill(e)
                for i in range(8):
                    a = fa - half + (half * 2 * i / 7)
                    self.particles.append(Particle(
                        self.player.x + math.cos(a) * weapon.whip_range * random.uniform(0.3, 1.0),
                        self.player.y + math.sin(a) * weapon.whip_range * random.uniform(0.3, 1.0),
                        weapon.defn["color"], life=10, size=3))

            elif wtype == "meteor":
                # Drop meteors on random enemies
                targets = [e for e in self.enemies if e.alive]
                if targets:
                    for _ in range(weapon.proj_count):
                        t = random.choice(targets)
                        aoe_r = weapon.aoe_radius
                        for e in self.enemies:
                            if not e.alive:
                                continue
                            if math.hypot(e.x - t.x, e.y - t.y) < aoe_r:
                                if e.take_damage(total_dmg):
                                    self._on_kill(e)
                        for _ in range(12):
                            a = random.uniform(0, math.pi * 2)
                            r = random.uniform(0, aoe_r)
                            self.particles.append(Particle(
                                t.x + math.cos(a) * r, t.y + math.sin(a) * r,
                                ORANGE, life=15, size=5))
                        self.add_shake(3)
                        self.floating_texts.append(FloatingText(
                            t.x, t.y - 30, str(total_dmg), ORANGE, life=20, size=16))

            elif wtype == "orbit":
                radius = weapon.orbit_radius
                count = weapon.orbit_count
                for i in range(count):
                    a = self.frame * 0.08 + (i * 2 * math.pi / count)
                    bx = self.player.x + math.cos(a) * radius
                    by = self.player.y + math.sin(a) * radius
                    for e in self.enemies:
                        if not e.alive:
                            continue
                        if math.hypot(e.x - bx, e.y - by) < 30:
                            if e.take_damage(total_dmg):
                                self._on_kill(e)

            elif wtype == "chain":
                # Chain lightning: bounces between enemies
                chain_range = weapon.chain_range
                chain_count = weapon.chain_count
                nearest = self._nearest_enemy()
                if nearest:
                    hit_set = set()
                    current = nearest
                    for _ in range(chain_count):
                        if id(current) in hit_set or not current.alive:
                            break
                        hit_set.add(id(current))
                        if current.take_damage(total_dmg):
                            self._on_kill(current)
                        # Draw chain visual
                        for _ in range(3):
                            self.particles.append(Particle(
                                current.x, current.y, CYAN, life=8, size=3))
                        # Find next target
                        best_next, best_d = None, chain_range
                        for e in self.enemies:
                            if not e.alive or id(e) in hit_set:
                                continue
                            d = math.hypot(e.x - current.x, e.y - current.y)
                            if d < best_d:
                                best_d, best_next = d, e
                        if best_next:
                            # Chain line visual
                            steps = max(1, int(best_d / 20))
                            for s in range(steps):
                                t = s / steps
                                px = current.x + (best_next.x - current.x) * t
                                py = current.y + (best_next.y - current.y) * t
                                self.particles.append(Particle(
                                    px, py, CYAN, life=10, size=2))
                        current = best_next

            elif wtype == "homing":
                # Homing projectiles that seek enemies
                targets = [e for e in self.enemies if e.alive]
                for t in targets[:weapon.proj_count]:
                    a = math.atan2(t.y - self.player.y, t.x - self.player.x)
                    spd = weapon.defn["proj_speed"]
                    p = HomingProjectile(
                        self.player.x, self.player.y,
                        math.cos(a) * spd, math.sin(a) * spd,
                        total_dmg, weapon, turn_speed=0.12)
                    self.projectiles.append(p)

            elif wtype == "radial":
                # Fire in all directions evenly
                n = weapon.proj_count
                for i in range(n):
                    a = (i * 2 * math.pi / n) + self.frame * 0.05
                    spd = weapon.defn["proj_speed"]
                    self.projectiles.append(Projectile(
                        self.player.x, self.player.y,
                        math.cos(a) * spd, math.sin(a) * spd,
                        total_dmg, weapon))

    def _nearest_enemy(self):
        nearest, best = None, float('inf')
        for e in self.enemies:
            if not e.alive:
                continue
            d = math.hypot(e.x - self.player.x, e.y - self.player.y)
            if d < best:
                best, nearest = d, e
        return nearest

    def _on_kill(self, enemy):
        self.kill_count += 1
        self.bestiary_killed.add(enemy.etype)

        # Combo system
        self.combo_count += 1
        self.combo_timer = 90  # 1.5 seconds to maintain combo
        self.combo_mult = 1.0 + (self.combo_count - 1) * 0.1
        self.combo_mult = min(self.combo_mult, 5.0)
        self.max_combo = max(self.max_combo, self.combo_count)

        # XP with combo multiplier
        xp_val = int(enemy.xp_value * self.combo_mult)
        self.xp_gems.append(XPGem(enemy.x, enemy.y, xp_val))

        # Drops
        luck = self.player.luck
        if random.random() < 0.07 + luck * 0.01:
            self.health_pickups.append(HealthPickup(enemy.x, enemy.y))
        # Chest drops
        chest_chance = 0.005 + luck * 0.002
        if enemy.is_boss:
            chest_chance = 1.0
        if random.random() < chest_chance:
            if enemy.is_boss:
                rarity = random.choices(["rare", "epic", "legendary"], [3, 4, 3])[0]
            else:
                rarity = random.choices(["common", "rare", "epic"], [10, 3, 1])[0]
            self.chest_pickups.append(ChestPickup(enemy.x, enemy.y, rarity))

        # Death particles
        for _ in range(8):
            self.particles.append(Particle(
                enemy.x, enemy.y, enemy.color,
                dx=random.uniform(-3, 3), dy=random.uniform(-3, 3),
                life=20, size=4))

        # On death effects (splits, explosions)
        spawns = enemy.on_death(self)
        for stype, sx, sy in spawns:
            e = Enemy(sx, sy, stype, 1.0 + (self.wave - 1) * 0.1)
            e._game = self
            self.enemies.append(e)

        # Combo text
        if self.combo_count > 2:
            self.floating_texts.append(FloatingText(
                enemy.x + random.randint(-10, 10), enemy.y - 25,
                f"x{self.combo_count} +{xp_val}xp", GOLD if self.combo_count > 10 else YELLOW,
                life=35, size=14 + min(self.combo_count, 20)))

    # ── COLLISIONS ──
    def check_collisions(self):
        # Projectiles vs Enemies
        for proj in self.projectiles:
            if not proj.alive:
                continue
            for enemy in self.enemies:
                if not enemy.alive or id(enemy) in proj.hit_enemies:
                    continue
                if math.hypot(proj.x - enemy.x, proj.y - enemy.y) < 25:
                    proj.hit_enemies.add(id(enemy))
                    killed = enemy.take_damage(proj.damage)
                    self.total_dmg_dealt += proj.damage
                    d = math.hypot(proj.x - enemy.x, proj.y - enemy.y) + 0.01
                    enemy.knockback_x += (enemy.x - proj.x) / d * 2
                    enemy.knockback_y += (enemy.y - proj.y) / d * 2
                    color = GOLD if proj.damage > (enemy.max_hp * 0.3) else WHITE
                    self.floating_texts.append(FloatingText(
                        enemy.x + random.randint(-10, 10), enemy.y - 25,
                        str(proj.damage), color, life=25, size=18))
                    # AOE for fireball
                    if proj.weapon.defn.get("aoe_radius") and proj.weapon.defn["type"] == "projectile":
                        aoe_r = proj.weapon.aoe_radius
                        for e2 in self.enemies:
                            if not e2.alive or e2 is enemy:
                                continue
                            if math.hypot(proj.x - e2.x, proj.y - e2.y) < aoe_r:
                                if e2.take_damage(proj.damage // 2):
                                    self._on_kill(e2)
                        for _ in range(15):
                            a = random.uniform(0, math.pi * 2)
                            r = random.uniform(0, aoe_r)
                            self.particles.append(Particle(
                                proj.x + math.cos(a) * r,
                                proj.y + math.sin(a) * r,
                                ORANGE, life=15, size=5))
                        self.add_shake(5)
                        proj.alive = False
                    if killed:
                        self._on_kill(enemy)
                    proj.pierce -= 1
                    if proj.pierce <= 0:
                        proj.alive = False
                    break

        # Puddles vs Enemies
        for puddle in self.puddles:
            if not puddle.alive:
                continue
            for enemy in self.enemies:
                if not enemy.alive or id(enemy) in puddle.hit_set:
                    continue
                if math.hypot(enemy.x - puddle.x, enemy.y - puddle.y) < puddle.radius:
                    puddle.hit_set.add(id(enemy))
                    if enemy.take_damage(puddle.weapon.damage + self.player.damage_bonus):
                        self._on_kill(enemy)

        # Enemies vs Player
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            if math.hypot(enemy.x - self.player.x, enemy.y - self.player.y) < 30:
                if self.player.take_damage(enemy.damage):
                    self.add_shake(4)
                    self.floating_texts.append(FloatingText(
                        self.player.x, self.player.y - 30,
                        str(enemy.damage), RED, life=30, size=20))
                    d = math.hypot(enemy.x - self.player.x, enemy.y - self.player.y) + 0.01
                    enemy.knockback_x -= (enemy.x - self.player.x) / d * 5
                    enemy.knockback_y -= (enemy.y - self.player.y) / d * 5
                    enemy.on_hit_player(self.player, self)

        # XP gems
        for gem in self.xp_gems:
            if not gem.alive:
                continue
            gem.magnet_range = self.player.pickup_range
            xp = gem.update(self.player, self.frame)
            if xp > 0:
                if self.player.gain_xp(xp):
                    self.level_up_pending = True
                    self._check_milestones()
                    self._gen_upgrades()

        # Health pickups
        for hp in self.health_pickups:
            if not hp.alive:
                continue
            hp.update()
            if math.hypot(hp.x - self.player.x, hp.y - self.player.y) < 30:
                healed = min(hp.heal_amount, self.player.max_hp - self.player.hp)
                self.player.hp = min(self.player.hp + hp.heal_amount, self.player.max_hp)
                hp.alive = False
                self.floating_texts.append(FloatingText(
                    hp.x, hp.y - 20, f"+{healed}HP", GREEN, life=20, size=16))

        # Chest pickups
        for chest in self.chest_pickups:
            if not chest.alive or chest.opened:
                continue
            chest.update()
            if math.hypot(chest.x - self.player.x, chest.y - self.player.y) < 40:
                chest.opened = True
                self._open_chest(chest)

        # Update enemy slow timers
        for e in self.enemies:
            if hasattr(e, '_slow_timer') and e._slow_timer > 0:
                e._slow_timer -= 1
                if e._slow_timer <= 0:
                    e.speed = e.base_speed

    def _open_chest(self, chest):
        """Open a chest and give rewards."""
        if chest.rarity == "common":
            # Small XP bonus + chance for reroll
            bonus_xp = 20 + self.wave * 5
            self.player.gain_xp(bonus_xp)
            self.floating_texts.append(FloatingText(chest.x, chest.y - 20, f"+{bonus_xp}xp", YELLOW, life=30, size=18))
            if random.random() < 0.3:
                self.player.rerolls += 1
                self.floating_texts.append(FloatingText(chest.x, chest.y - 40, "+1 Reroll", CYAN, life=30, size=14))
        elif chest.rarity == "rare":
            bonus_xp = 50 + self.wave * 10
            self.player.gain_xp(bonus_xp)
            self.floating_texts.append(FloatingText(chest.x, chest.y - 20, f"+{bonus_xp}xp", BLUE, life=30, size=18))
            self.player.rerolls += 1
            self.floating_texts.append(FloatingText(chest.x, chest.y - 40, "+1 Reroll", CYAN, life=30, size=14))
        elif chest.rarity == "epic":
            bonus_xp = 100 + self.wave * 15
            self.player.gain_xp(bonus_xp)
            self.player.hp = min(self.player.hp + 30, self.player.max_hp)
            self.floating_texts.append(FloatingText(chest.x, chest.y - 20, f"+{bonus_xp}xp +30HP", PURPLE, life=30, size=18))
            self.player.rerolls += 2
            self.floating_texts.append(FloatingText(chest.x, chest.y - 40, "+2 Rerolls", CYAN, life=30, size=14))
        elif chest.rarity == "legendary":
            bonus_xp = 200 + self.wave * 20
            self.player.gain_xp(bonus_xp)
            self.player.hp = self.player.max_hp
            self.floating_texts.append(FloatingText(chest.x, chest.y - 20, f"FULL HEAL +{bonus_xp}xp", GOLD, life=40, size=20))
            self.player.rerolls += 3
            self.player.crit_mult += 0.3
            self.floating_texts.append(FloatingText(chest.x, chest.y - 45, "+3 Rerolls +Crit", GOLD, life=40, size=16))
        self.add_shake(3)

    def _check_milestones(self):
        lvl = self.player.level
        if lvl in MILESTONE_REWARDS:
            kind, text = MILESTONE_REWARDS[lvl]
            self.milestone_queue.append((kind, text))
            if not self.milestone_display_timer:
                self._apply_next_milestone()

    def _apply_next_milestone(self):
        if not self.milestone_queue:
            return
        kind, text = self.milestone_queue.pop(0)
        if kind == "reroll":
            count = int(text.split("+")[1])
            self.player.rerolls += count
            self.milestone_display_text = f"MILESTONE: +{count} Reroll(s)!"
        elif kind == "weapon_slot":
            self.player.max_weapons += 1
            self.milestone_display_text = "MILESTONE: Max Weapons +1!"
        elif kind == "heal_full":
            self.player.hp = self.player.max_hp
            if "Reroll" in text:
                r = int(text.split("+")[-1].split()[0])
                self.player.rerolls += r
            self.milestone_display_text = f"MILESTONE: Full Heal! {text}"
        self.milestone_display_timer = 180

    def add_shake(self, intensity):
        self.screen_shake = max(self.screen_shake, intensity)

    # ── UPGRADE SYSTEM ──
    def _gen_upgrades(self):
        self.upgrade_choices = []
        pool = []
        for w in self.player.weapons:
            if w.level < 8:
                pool.append(("upgrade", w.id, w))
        owned = {w.id for w in self.player.weapons}
        for wid in ALL_WEAPONS:
            if wid not in owned:
                pool.append(("new", wid, None))
        pool += [("stat", s, None) for s in
                 ["max_hp", "speed", "armor", "regen", "damage",
                  "pickup_range", "crit_chance", "crit_mult", "luck", "cdr"]]
        random.shuffle(pool)
        self.upgrade_choices = pool[:3]

    def _reroll_upgrades(self):
        if self.player.rerolls > 0:
            self.player.rerolls -= 1
            self._gen_upgrades()

    def apply_upgrade(self, choice):
        kind, item_id, wi = choice
        if kind == "upgrade" and wi:
            wi.level += 1
            wi._recalc()
        elif kind == "new":
            self.player.add_weapon(item_id)
        elif kind == "stat":
            p = self.player
            if item_id == "max_hp":       p.max_hp += 20; p.hp = min(p.hp + 20, p.max_hp)
            elif item_id == "speed":      p.speed += 0.2
            elif item_id == "armor":      p.armor += 2
            elif item_id == "regen":      p.regen += 1
            elif item_id == "damage":     p.damage_bonus += 3
            elif item_id == "pickup_range": p.pickup_range += 25
            elif item_id == "crit_chance": p.crit_chance = min(0.6, p.crit_chance + 0.04)
            elif item_id == "crit_mult":  p.crit_mult += 0.25
            elif item_id == "luck":       p.luck += 1
            elif item_id == "cdr":        p.cdr = min(0.5, p.cdr + 0.05)

    # ── WAVE SYSTEM ──
    def update_wave(self):
        self.wave_timer += 1
        self.game_time += 1

        # Combo decay
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0
            self.combo_mult = 1.0

        # Biome update
        new_biome_idx = 0
        for i, b in enumerate(BIOMES):
            if self.wave >= b["wave"]:
                new_biome_idx = i
        if new_biome_idx != self.biome_idx:
            self.biome_idx = new_biome_idx
            self.biome = BIOMES[new_biome_idx]
            self.wave_announce_timer = 180
            self.wave_announce_text = f"~ {self.biome['name']} ~"

        # Wave transition
        if self.wave_timer >= self.wave_duration:
            self.wave_timer = 0
            self.wave += 1
            self.add_shake(8)
            self.wave_announce_timer = 120
            self.wave_announce_text = f"Wave {self.wave}"
            if self.wave % 5 == 0:
                self.spawn_boss()

        # Spawn enemies
        rate = max(6, 35 - self.wave * 2)
        self.spawn_timer += 1
        if self.spawn_timer >= rate:
            self.spawn_timer = 0
            count = 1 + self.wave // 2
            for _ in range(count):
                self.spawn_enemy()

        # Announce timers
        if self.wave_announce_timer > 0:
            self.wave_announce_timer -= 1
        if self.new_enemy_announce_timer > 0:
            self.new_enemy_announce_timer -= 1
        if self.milestone_display_timer > 0:
            self.milestone_display_timer -= 1
            if self.milestone_display_timer <= 0 and self.milestone_queue:
                self._apply_next_milestone()

    # ── DRAWING ──
    def draw_ground(self):
        self.screen.fill(self.biome["bg"])
        cam = self.camera
        grid_col = self.biome["grid"]
        sx_start = int(cam.x // 80) * 80
        sy_start = int(cam.y // 80) * 80
        for gx in range(sx_start, sx_start + SCREEN_W + 80, 80):
            sx, _ = cam.apply(gx, 0)
            pygame.draw.line(self.screen, grid_col, (sx, 0), (sx, SCREEN_H))
        for gy in range(sy_start, sy_start + SCREEN_H + 80, 80):
            _, sy = cam.apply(0, gy)
            pygame.draw.line(self.screen, grid_col, (0, sy), (SCREEN_W, sy))

    def draw_hud(self):
        hud = pygame.Surface((SCREEN_W, 58), pygame.SRCALPHA)
        hud.fill(HUD_BG)
        self.screen.blit(hud, (0, 0))

        p = self.player
        # HP bar
        hp_w, hp_h, hp_x, hp_y = 200, 18, 15, 8
        pygame.draw.rect(self.screen, DARK_RED, (hp_x, hp_y, hp_w, hp_h), border_radius=4)
        hw = max(0, int(hp_w * p.hp / p.max_hp))
        hp_col = GREEN if p.hp > p.max_hp * 0.5 else YELLOW if p.hp > p.max_hp * 0.25 else RED
        if hw > 0:
            pygame.draw.rect(self.screen, hp_col, (hp_x, hp_y, hw, hp_h), border_radius=4)
        ht = self.font_sm.render(f"HP {p.hp}/{p.max_hp}", True, WHITE)
        self.screen.blit(ht, (hp_x + hp_w // 2 - ht.get_width() // 2, hp_y + 1))

        # XP bar
        xp_w, xp_h, xp_y = 200, 10, hp_y + hp_h + 3
        pygame.draw.rect(self.screen, (30, 30, 80), (hp_x, xp_y, xp_w, xp_h), border_radius=3)
        xw = max(0, int(xp_w * p.xp / p.xp_to_next))
        if xw > 0:
            pygame.draw.rect(self.screen, BLUE, (hp_x, xp_y, xw, xp_h), border_radius=3)
        lt = self.font_sm.render(f"Lv.{p.level}", True, CYAN)
        self.screen.blit(lt, (hp_x + xp_w + 8, xp_y - 2))

        # Timer & Wave
        m, s = divmod(self.game_time // FPS, 60)
        tt = self.font_md.render(f"{m:02d}:{s:02d}", True, WHITE)
        self.screen.blit(tt, (SCREEN_W // 2 - tt.get_width() // 2, 3))
        wt = self.font_sm.render(f"Wave {self.wave} | {self.biome['name']}", True, ORANGE)
        self.screen.blit(wt, (SCREEN_W // 2 - wt.get_width() // 2, 28))

        # Combo
        if self.combo_count > 1:
            combo_col = GOLD if self.combo_mult >= 3.0 else YELLOW if self.combo_mult >= 2.0 else WHITE
            ct = self.font_md.render(f"x{self.combo_count} ({self.combo_mult:.1f}x)", True, combo_col)
            self.screen.blit(ct, (SCREEN_W // 2 - ct.get_width() // 2, 44))

        # Right side stats
        kt = self.font_sm.render(f"Kills: {self.kill_count}", True, WHITE)
        self.screen.blit(kt, (SCREEN_W - 140, 5))
        ac = sum(1 for e in self.enemies if e.alive)
        et = self.font_sm.render(f"Enemies: {ac}", True, WHITE)
        self.screen.blit(et, (SCREEN_W - 140, 22))
        bt = self.font_xs.render(f"Bestiary: {len(self.bestiary_killed)}/{len(ENEMY_TYPES)+len(BOSS_TYPES)}", True, LIGHT_GRAY)
        self.screen.blit(bt, (SCREEN_W - 180, 40))

        # Weapon bar
        wx = 15
        wy = SCREEN_H - 45
        for w in p.weapons:
            bg = pygame.Surface((44, 44), pygame.SRCALPHA)
            bg.fill((30, 24, 45, 200))
            pygame.draw.rect(bg, w.defn["color"], (0, 0, 44, 44), 2, border_radius=6)
            self.screen.blit(bg, (wx, wy))
            ts = emoji_font_sm.render(w.defn["emoji"], True, WHITE)
            self.screen.blit(ts, (wx + 4, wy + 2))
            lv = self.font_sm.render(f"Lv{w.level}", True, w.defn["color"])
            self.screen.blit(lv, (wx + 22, wy + 26))
            wx += 50

        # Rerolls
        if p.rerolls > 0:
            rt = self.font_sm.render(f"Rerolls: {p.rerolls} [T]", True, CYAN)
            self.screen.blit(rt, (wx + 10, wy + 14))

        # Stats bar
        stats = []
        if p.armor > 0:     stats.append(f"Armor:{p.armor}")
        if p.regen > 0:     stats.append(f"Regen:{p.regen}/s")
        if p.crit_chance > 0.05: stats.append(f"Crit:{int(p.crit_chance*100)}%")
        if p.cdr > 0:       stats.append(f"CDR:{int(p.cdr*100)}%")
        if p.luck > 0:      stats.append(f"Luck:{p.luck}")
        sx_pos = SCREEN_W - 180
        sy_pos = SCREEN_H - 45
        for i, s in enumerate(stats):
            st = self.font_xs.render(s, True, LIGHT_GRAY)
            self.screen.blit(st, (sx_pos, sy_pos + i * 14))

        # Wave progress
        bar_w = SCREEN_W - 20
        bar_y = 55
        progress = self.wave_timer / self.wave_duration
        pygame.draw.rect(self.screen, (40, 30, 60), (10, bar_y, bar_w, 3))
        pw = int(bar_w * progress)
        if pw > 0:
            col = ORANGE if self.wave % 5 == 4 else CYAN
            pygame.draw.rect(self.screen, col, (10, bar_y, pw, 3))

    def draw_minimap(self):
        mm = 120
        mx, my = SCREEN_W - mm - 10, 68
        ms = pygame.Surface((mm, mm), pygame.SRCALPHA)
        ms.fill((0, 0, 0, 120))
        scale = 0.05
        cx, cy = mm // 2, mm // 2
        pygame.draw.circle(ms, GREEN, (cx, cy), 3)
        for e in self.enemies:
            if not e.alive:
                continue
            ex = int(cx + (e.x - self.player.x) * scale)
            ey = int(cy + (e.y - self.player.y) * scale)
            if 0 <= ex < mm and 0 <= ey < mm:
                c = GOLD if e.is_boss else RED
                r = 3 if e.is_boss else 2
                pygame.draw.circle(ms, c, (ex, ey), r)
        for gem in self.xp_gems:
            if not gem.alive:
                continue
            gx = int(cx + (gem.x - self.player.x) * scale)
            gy = int(cy + (gem.y - self.player.y) * scale)
            if 0 <= gx < mm and 0 <= gy < mm:
                pygame.draw.circle(ms, BLUE, (gx, gy), 1)
        for ch in self.chest_pickups:
            if not ch.alive or ch.opened:
                continue
            chx = int(cx + (ch.x - self.player.x) * scale)
            chy = int(cy + (ch.y - self.player.y) * scale)
            if 0 <= chx < mm and 0 <= chy < mm:
                pygame.draw.rect(ms, ch.color, (chx-2, chy-2, 4, 4))
        pygame.draw.rect(ms, (80, 80, 120), (0, 0, mm, mm), 1)
        self.screen.blit(ms, (mx, my))

    def draw_announcements(self):
        y = SCREEN_H // 2 - 100
        if self.wave_announce_timer > 0:
            alpha = min(255, self.wave_announce_timer * 4)
            ts = self.font_lg.render(self.wave_announce_text, True, ORANGE)
            ts.set_alpha(alpha)
            self.screen.blit(ts, (SCREEN_W // 2 - ts.get_width() // 2, y))
            y += 50

        if self.new_enemy_announce_timer > 0:
            alpha = min(255, self.new_enemy_announce_timer * 3)
            emoji_ts = emoji_font.render(self.new_enemy_announce_emoji, True, WHITE)
            emoji_ts.set_alpha(alpha)
            name_ts = self.font_md.render(f"NEW: {self.new_enemy_announce_name}", True, PINK)
            name_ts.set_alpha(alpha)
            self.screen.blit(emoji_ts, (SCREEN_W // 2 - 60, y))
            self.screen.blit(name_ts, (SCREEN_W // 2 - name_ts.get_width() // 2 + 20, y + 5))
            y += 50

        if self.milestone_display_timer > 0:
            alpha = min(255, self.milestone_display_timer * 4)
            ms = self.font_lg.render(self.milestone_display_text, True, GOLD)
            ms.set_alpha(alpha)
            self.screen.blit(ms, (SCREEN_W // 2 - ms.get_width() // 2, y))

    def draw_level_up(self):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 150))
        self.screen.blit(ov, (0, 0))

        title = self.font_lg.render(f"LEVEL UP! (Lv.{self.player.level})", True, YELLOW)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 100))
        sub = self.font_md.render("Choose an upgrade:", True, WHITE)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 150))
        if self.player.rerolls > 0:
            rr = self.font_sm.render(f"Press [T] to Reroll ({self.player.rerolls} left)", True, CYAN)
            self.screen.blit(rr, (SCREEN_W // 2 - rr.get_width() // 2, 178))

        cw, ch = 300, 220
        total = len(self.upgrade_choices) * (cw + 15) - 15
        sx = SCREEN_W // 2 - total // 2
        mx_pos, my_pos = pygame.mouse.get_pos()

        for i, choice in enumerate(self.upgrade_choices):
            kind, item_id, wi = choice
            cx = sx + i * (cw + 15)
            cy = 210
            hovered = cx <= mx_pos <= cx + cw and cy <= my_pos <= cy + ch
            bg_col = (80, 60, 120) if hovered else (50, 38, 75)

            card = pygame.Surface((cw, ch), pygame.SRCALPHA)
            card.fill((*bg_col, 240))
            bc = YELLOW if hovered else (100, 80, 140)
            pygame.draw.rect(card, bc, (0, 0, cw, ch), 3, border_radius=12)
            self.screen.blit(card, (cx, cy))

            if kind == "upgrade" and wi:
                d = WEAPON_DEFS[item_id]
                emoji_str = d["emoji"]
                name = f"{d['name']} Lv.{wi.level + 1}"
                desc = d["desc"]
                nd = wi.damage + int(wi.defn["base_damage"] * 0.25)
                details = [f"DMG: {wi.damage} -> {nd}"]
                if wi.defn.get("proj_count"):
                    nc = wi.proj_count + (1 if (wi.level) % 2 == 0 else 0)
                    details.append(f"Proj: {wi.proj_count} -> {nc}")
            elif kind == "new":
                d = WEAPON_DEFS[item_id]
                emoji_str = d["emoji"]
                name = f"NEW: {d['name']}"
                desc = d["desc"]
                details = [f"DMG: {d['base_damage']}", f"CD: {d['base_cooldown']}s"]
            else:
                stat_map = {
                    "max_hp": ("\u2764", "Max HP +20", "Increases maximum health"),
                    "speed": ("\U0001f45f", "Speed +0.2", "Move faster to dodge"),
                    "armor": ("\U0001f6e1", "Armor +2", "Reduce damage taken"),
                    "regen": ("\U0001f49a", "Regen +1/s", "Heal over time"),
                    "damage": ("\u2694", "Damage +3", "All weapons hit harder"),
                    "pickup_range": ("\U0001f9f2", "Pickup +25", "Collect XP from further"),
                    "crit_chance": ("\u2728", "Crit +4%", "More critical hits"),
                    "crit_mult": ("\U0001f531", "Crit DMG +25%", "Deadlier crits"),
                    "luck": ("\U0001f340", "Luck +1", "Better drop rates"),
                    "cdr": ("\u23f1", "CDR +5%", "Weapons fire faster"),
                }
                emoji_str, name, desc = stat_map.get(item_id, ("?", "?", "?"))
                details = []

            ts = emoji_font_lg.render(emoji_str, True, WHITE)
            self.screen.blit(ts, (cx + cw // 2 - ts.get_width() // 2, cy + 10))
            nt = self.font_md.render(name, True, YELLOW if kind == "new" else WHITE)
            self.screen.blit(nt, (cx + cw // 2 - nt.get_width() // 2, cy + 65))
            dt = self.font_sm.render(desc, True, LIGHT_GRAY)
            self.screen.blit(dt, (cx + cw // 2 - dt.get_width() // 2, cy + 95))
            for j, det in enumerate(details):
                ddt = self.font_sm.render(det, True, GREEN)
                self.screen.blit(ddt, (cx + cw // 2 - ddt.get_width() // 2, cy + 125 + j * 18))
            kt = self.font_sm.render(f"[{i + 1}] or Click", True, CYAN)
            self.screen.blit(kt, (cx + cw // 2 - kt.get_width() // 2, cy + ch - 22))

    def draw_game_over(self):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        self.screen.blit(ov, (0, 0))
        t = self.font_title.render("GAME OVER", True, RED)
        self.screen.blit(t, (SCREEN_W // 2 - t.get_width() // 2, 100))
        m, s = divmod(self.game_time // FPS, 60)
        stats = [
            f"Survived: {m:02d}:{s:02d}",
            f"Level: {self.player.level}",
            f"Kills: {self.kill_count}",
            f"Wave: {self.wave}",
            f"Max Combo: x{self.max_combo}",
            f"Bestiary: {len(self.bestiary_killed)}/{len(ENEMY_TYPES)+len(BOSS_TYPES)}",
            f"Total Damage: {self.total_dmg_dealt:,}",
            f"Biome Reached: {self.biome['name']}",
        ]
        for i, st in enumerate(stats):
            txt = self.font_md.render(st, True, WHITE)
            self.screen.blit(txt, (SCREEN_W // 2 - txt.get_width() // 2, 200 + i * 32))
        rt = self.font_md.render("[R] Restart   [Q] Quit", True, YELLOW)
        self.screen.blit(rt, (SCREEN_W // 2 - rt.get_width() // 2, 480))

    def draw_title_screen(self):
        self.screen.fill(DARK_BG)
        for i in range(50):
            x = (i * 97 + self.frame * (0.5 + i * 0.02)) % SCREEN_W
            y = (i * 53 + self.frame * (0.3 + i * 0.01)) % SCREEN_H
            pygame.draw.circle(self.screen, (40, 30, 60), (int(x), int(y)), 2)

        t = self.font_title.render("EMOJI SURVIVORS v3", True, YELLOW)
        self.screen.blit(t, (SCREEN_W // 2 - t.get_width() // 2, 80))

        sub = self.font_md.render("75 Enemy Types | 20 Weapons | 15 Biomes | 10 Tiers", True, LIGHT_GRAY)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 150))

        controls = [
            "WASD / Arrow Keys - Move",
            "Auto-attack nearest enemies",
            "Kill enemies for XP -> Level Up -> Upgrades",
            "[T] Reroll upgrade choices  |  [P] Pause",
            "Build combos for XP multiplier!",
            "",
            "Press ENTER or SPACE to start",
        ]
        for i, c in enumerate(controls):
            ct = self.font_md.render(c, True, WHITE if i < 5 else CYAN)
            self.screen.blit(ct, (SCREEN_W // 2 - ct.get_width() // 2, 210 + i * 30))

        # Show enemy tiers
        tier_labels = ["T1:1+", "T2:2+", "T3:4+", "T4:7+", "T5:12+",
                        "T6:18+", "T7:25+", "T8:35+", "T9:45+", "T10:60+"]
        tier_colors = [GREEN, CYAN, YELLOW, ORANGE, RED, PURPLE, GOLD, (255,150,255), PINK, WHITE]
        cols_per_row = 5
        for i, (label, col) in enumerate(zip(tier_labels, tier_colors)):
            tx = 100 + (i % cols_per_row) * 220
            ty = 420 + (i // cols_per_row) * 28
            lt = self.font_sm.render(label, True, col)
            self.screen.blit(lt, (tx, ty))

        # Enemy showcase (cycle through enemies)
        all_e = list(ENEMY_TYPES.keys())
        show = all_e[:16]
        ex_start = SCREEN_W // 2 - len(show) * 20
        for i, etype in enumerate(show):
            ts = emoji_font_sm.render(ENEMY_TYPES[etype]["emoji"], True, WHITE)
            col = i % 8
            row = i // 8
            self.screen.blit(ts, (ex_start + col * 50, 520 + row * 40))

        more = self.font_sm.render(f"...and {len(ENEMY_TYPES) - 16} more enemies across 10 tiers!", True, LIGHT_GRAY)
        self.screen.blit(more, (SCREEN_W // 2 - more.get_width() // 2, 620))

        feat = self.font_sm.render("Features: Combos | Crits | Rerolls | Chests | Bestiary | Biomes | Chain Lightning | Homing | Radial", True, GRAY)
        self.screen.blit(feat, (SCREEN_W // 2 - feat.get_width() // 2, 660))

    # ── MAIN LOOP ──
    def run(self):
        running = True
        in_title = True
        while running:
            self.frame += 1
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if in_title:
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            in_title = False
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                        continue

                    if event.key == pygame.K_ESCAPE:
                        if self.level_up_pending:
                            self.level_up_pending = False
                        else:
                            running = False
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_t and self.level_up_pending:
                        self._reroll_upgrades()

                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.__init__()
                            in_title = False
                        elif event.key == pygame.K_q:
                            running = False

                    if self.level_up_pending:
                        for idx in range(min(3, len(self.upgrade_choices))):
                            if event.key == pygame.K_1 + idx:
                                self.apply_upgrade(self.upgrade_choices[idx])
                                self.level_up_pending = False

                elif event.type == pygame.MOUSEBUTTONDOWN and self.level_up_pending:
                    mx, my = pygame.mouse.get_pos()
                    cw, ch_card = 300, 220
                    total = len(self.upgrade_choices) * (cw + 15) - 15
                    sx = SCREEN_W // 2 - total // 2
                    for i in range(len(self.upgrade_choices)):
                        cx = sx + i * (cw + 15)
                        cy = 210
                        if cx <= mx <= cx + cw and cy <= my <= cy + ch_card:
                            self.apply_upgrade(self.upgrade_choices[i])
                            self.level_up_pending = False
                            break

            if in_title:
                self.draw_title_screen()
                pygame.display.flip()
                continue

            if self.paused:
                self.draw_ground()
                self.player.draw(self.screen, self.camera)
                self.draw_hud()
                pt = self.font_lg.render("PAUSED", True, WHITE)
                self.screen.blit(pt, (SCREEN_W // 2 - pt.get_width() // 2, SCREEN_H // 2))
                pygame.display.flip()
                continue

            if self.game_over:
                self.draw_ground()
                for e in self.enemies:
                    e.draw(self.screen, self.camera)
                self.player.draw(self.screen, self.camera)
                self.draw_hud()
                self.draw_game_over()
                pygame.display.flip()
                continue

            if self.level_up_pending:
                self.draw_ground()
                for p in self.puddles: p.draw(self.screen, self.camera)
                for gem in self.xp_gems: gem.draw(self.screen, self.camera, self.frame)
                for hp in self.health_pickups: hp.draw(self.screen, self.camera)
                for ch in self.chest_pickups: ch.draw(self.screen, self.camera, self.frame)
                for e in self.enemies: e.draw(self.screen, self.camera)
                self.player.draw(self.screen, self.camera)
                for proj in self.projectiles: proj.draw(self.screen, self.camera)
                for p in self.particles: p.draw(self.screen, self.camera)
                for ft in self.floating_texts: ft.draw(self.screen, self.camera)
                self.draw_hud()
                self.draw_minimap()
                self.draw_announcements()
                self.draw_level_up()
                pygame.display.flip()
                continue

            # ── UPDATE ──
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.camera.update(self.player.x, self.player.y)
            self.update_wave()

            for e in self.enemies:
                if e.alive:
                    e.update(self.player, self.enemies)

            self.process_weapons()

            for p in self.projectiles:
                if p.alive:
                    if isinstance(p, HomingProjectile):
                        p.update(self.player, self.enemies)
                    else:
                        p.update(self.player)
            for p in self.puddles:
                if p.alive:
                    p.update(dt)

            self.particles = [p for p in self.particles if p.update()]
            self.floating_texts = [ft for ft in self.floating_texts if ft.update()]

            self.check_collisions()

            self.enemies = [e for e in self.enemies if e.alive]
            self.projectiles = [p for p in self.projectiles if p.alive]
            self.puddles = [p for p in self.puddles if p.alive]
            self.xp_gems = [g for g in self.xp_gems if g.alive]
            self.health_pickups = [h for h in self.health_pickups if h.alive]
            self.chest_pickups = [c for c in self.chest_pickups if c.alive]

            if self.player.hp <= 0:
                self.game_over = True

            # Screen shake
            if self.screen_shake > 0:
                self.shake_x = random.randint(-self.screen_shake, self.screen_shake)
                self.shake_y = random.randint(-self.screen_shake, self.screen_shake)
                self.screen_shake -= 1
            else:
                self.shake_x = self.shake_y = 0

            # ── DRAW ──
            self.camera.x += self.shake_x
            self.camera.y += self.shake_y

            self.draw_ground()
            for p in self.puddles: p.draw(self.screen, self.camera)
            for gem in self.xp_gems: gem.draw(self.screen, self.camera, self.frame)
            for hp in self.health_pickups: hp.draw(self.screen, self.camera)
            for ch in self.chest_pickups: ch.draw(self.screen, self.camera, self.frame)
            for e in self.enemies: e.draw(self.screen, self.camera)
            self.player.draw(self.screen, self.camera)
            for proj in self.projectiles: proj.draw(self.screen, self.camera)
            for p in self.particles: p.draw(self.screen, self.camera)
            for ft in self.floating_texts: ft.draw(self.screen, self.camera)

            self.camera.x -= self.shake_x
            self.camera.y -= self.shake_y

            self.draw_hud()
            self.draw_minimap()
            self.draw_announcements()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


# ─── GLOBAL FONTS ──────────────────────────────────────────────────────────────
def find_emoji_font(size):
    candidates = [
        "Noto Color Emoji", "Segoe UI Emoji", "Apple Color Emoji",
        "Android Emoji", "Twemoji Mozilla", "Segoe UI Symbol",
        "Symbola", "Noto Sans SC", "WenQuanYi Micro Hei",
        "Noto Emoji", "DejaVu Sans", "Arial Unicode MS", None,
    ]
    for name in candidates:
        try:
            f = pygame.font.SysFont(name, size)
            f.render("\u2694\u26a1\U0001f525", True, (255, 255, 255))
            return f
        except Exception:
            continue
    return pygame.font.Font(None, size)


if __name__ == "__main__":
    emoji_font = find_emoji_font(32)
    emoji_font_sm = find_emoji_font(22)
    emoji_font_lg = find_emoji_font(48)
    game = Game()
    game.run()