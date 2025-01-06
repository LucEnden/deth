const { Dex } = require('pokemon-showdown');
const fs = require('fs');

// const dex = Dex.mod('gen4');

// ALL keys in dex object
// console.log(Object.keys(dex));
// [
//     'Abilities',   'Rulesets',
//     'FormatsData', 'Items',
//     'Learnsets',   'Moves',
//     'Natures',     'Pokedex',
//     'Scripts',     'Conditions',
//     'TypeChart',   'Aliases'
// ]

// ALL keys in dex.species object
// const allKeys = new Set();
// pokemon.forEach(p => {
//     Object.keys(p).forEach(key => allKeys.add(key));
// });
// console.log([...allKeys]);
// [
//     'exists',           'tags',           'evoType',
//     'evoCondition',     'abilities',      'num',
//     'name',             'types',          'baseStats',
//     'heightm',          'weightkg',       'color',
//     'prevo',            'evoItem',        'eggGroups',
//     'tier',             'id',             'fullname',
//     'effectType',       'gen',            'shortDesc',
//     'desc',             'isNonstandard',  'duration',
//     'noCopy',           'affectsFainted', 'status',
//     'weather',          'sourceEffect',   'baseSpecies',
//     'forme',            'baseForme',      'cosmeticFormes',
//     'otherFormes',      'formeOrder',     'spriteid',
//     'addedType',        'doublesTier',    'natDexTier',
//     'evos',             'evoMove',        'evoLevel',
//     'nfe',              'canHatch',       'gender',
//     'genderRatio',      'requiredItem',   'requiredItems',
//     'bst',              'weighthg',       'unreleasedHidden',
//     'maleOnlyHidden',   'maxHP',          'isMega',
//     'canGigantamax',    'gmaxUnreleased', 'cannotDynamax',
//     'battleOnly',       'changesFrom',    'requiredAbility',
//     'onBeforeSwitchIn', 'onSwitchIn',     'evoRegion',
//     'isPrimal',         'requiredMove',   'onTypePriority',
//     'onType'
// ]

const dex = Dex.mod('gen4');
const pokemon = dex.species.all().filter(p => p.gen <= 4 && p.isNonstandard === null && p.baseSpecies === p.name);
pokemon.sort((a, b) => a.num - b.num);

const data = dex.loadData();

function parse_learnset(p) {
    var parsed_learnset = data['Learnsets'][p.id].learnset;
    var move_names = Object.keys(parsed_learnset);

    for (let i = 0; i < move_names.length; i++) {
        // Moves are formated as <generation><learned by><other>
        // Where <learned by> is M (machine), T (tutor), E (egg), L (level)
        // With level moves, <other> is the level learned
        parsed_learnset[move_names[i]] = parsed_learnset[move_names[i]].filter(m => m.startsWith('4'));

        if (parsed_learnset[move_names[i]].length === 0) {
            delete parsed_learnset[move_names[i]];
        }
    }

    // Recursively add pre-evolution learnsets to current learnset
    // if (p.prevo && data['Learnsets'][p.prevo.toLowerCase()]) {
    //     prevo = dex.species.get(p.prevo.toLowerCase());
    //     parsed_learnset = { ...parse_learnset(prevo), ...parsed_learnset };
    // }

    return parsed_learnset;
}

function gen4_dex_to_json() {
    const dex = Dex.mod('gen4');
    const pokemon = dex.species.all().filter(p => p.gen <= 4 && p.isNonstandard === null && p.baseSpecies === p.name);
    pokemon.sort((a, b) => a.num - b.num);
    pokemon.forEach(p => {
        p.learnset = parse_learnset(p);
    });

    // Remove unnecessary data
    const keys_to_keep = [
        'id', 'num', 'types', 'baseStats', 'abilities', 'weightkg', 'genderRatio', 'learnset'
    ]
    const gen4_dex = pokemon.map(p => {
        const new_p = {};
        keys_to_keep.forEach(key => {
            new_p[key] = p[key];
        });
        return new_p;
    })

    // Ensure no none values for gender
    gen4_dex.map(p => {
        if (p.gender === '') p.gender = 'MF';
        return p;
    })

    // Convert ability from object to array
    gen4_dex.map(p => {
        p.abilities = Object.values(p.abilities);
        return p;
    })

    const gen4_dex_json = {}
    for (p of gen4_dex) {
        let id = p.id;
        delete p.id;
        gen4_dex_json[id] = p;
    }

    // Save to JSON file
    const dex_fname = 'gen4_dex.json';
    fs.writeFileSync(dex_fname, JSON.stringify(gen4_dex_json));
    console.log('Gen 4 data successfully written to', dex_fname);
}

gen4_dex_to_json();