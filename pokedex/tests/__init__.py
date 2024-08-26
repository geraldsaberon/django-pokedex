sample_valid_form_data = {
    "name": "test",
    "type1": "grass",
    "type2": "poison",
    "ability1": "overgrow",
    "ability2": "chlorophyll",
    "hp": 0,
    "attack": 0,
    "defense": 0,
    "special_attack": 0,
    "special_defense": 0,
    "speed": 0
}

sample_valid_api_data = {
  "name": "test",
  "types":
  [
    {
      "type":
      {
        "name": "grass"
      },
      "slot": 1
    },
    {
      "type":
      {
        "name": "poison"
      },
      "slot": 2
    }
  ],
  "abilities":
  [
    {
      "name": "overgrow"
    },
    {
      "name": "chlorophyll"
    }
  ],
  "stats":
  [
    {
      "name": "hp",
      "base_stat": 60
    },
    {
      "name": "attack",
      "base_stat": 62
    },
    {
      "name": "defense",
      "base_stat": 63
    },
    {
      "name": "special-attack",
      "base_stat": 80
    },
    {
      "name": "special-defense",
      "base_stat": 80
    },
    {
      "name": "speed",
      "base_stat": 60
    }
  ]
}
