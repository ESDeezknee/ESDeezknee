<?php

namespace Database\Seeders;

use Illuminate\database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class IcebreakersSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        //
        $data = [
            [
                'id' => 1,
                'statements' => 'Go up to someone and compliment them.',
            ],
            [
                'id' => 2,
                'statements' => 'Tell the group a fun fact, everyone has to go',
            ],
            [
                'id' => 3,
                'statements' => 'Tell everyone what brings you joy and happiness',
            ],
            [
                'id' => 4,
                'statements' => 'Do the chicken dance',
            ],
            [
                'id' => 5,
                'statements' => 'Tell everyone a joke',
            ],
            [
                'id' => 6,
                'statements' => 'As the first step, you will need to hydrate and then tell everyone to hydrate. If you are able, recite the SAF 8 core values.',
            ]
            // Add more data here as needed
        ];
        DB::table('icebreakers')->insert($data);
        
    }
}
