<?php

namespace Database\Seeders;

use Illuminate\database\Console\Seeds\WithoutModelEvents;
use Illuminate\database\seeder;

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
                'statement' => 'Go up to someone and compliment them.',
            ],
            [
                'id' => 2,
                'statement' => 'Tell the group a fun fact, everyone has to go',
            ],
            [
                'id' => 3,
                'statement' => 'Tell everyone what brings you joy and happiness',
            ],
            [
                'id' => 4,
                'statement' => 'Do the chicken dance',
            ],
            [
                'id' => 5,
                'statement' => 'Tell everyone a joke',
            ],
            [
                'id' => 6,
                'statement' => 'As the first step, you will need to hydrate and then tell everyone to hydrate. If you are able, recite the SAF 8 core values.',
            ]
            // Add more data here as needed
        ];

        DB::table('statements')->insert($data);
    }
}
