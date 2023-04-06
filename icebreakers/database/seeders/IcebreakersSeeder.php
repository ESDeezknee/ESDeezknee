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
                'statements' => 'Aim: Look at how to be environmentally friendly today!',
            ],
            [
                'id' => 2,
                'statements' => 'Read up about Ecological Footprint and Environmental, Societal and Governance (ESG)',
            ],
            [
                'id' => 3,
                'statements' => 'What food do you hate to see in the bin and why?',
            ],
            [
                'id' => 4,
                'statements' => 'Educate your group mates on Carbon Sequestration.',
            ],
            [
                'id' => 5,
                'statements' => 'When using a squat toilet, do you face the door or face the flush?',
            ],
            [
                'id' => 6,
                'statements' => 'Find out what it means to have alternate energy! Share the findings with everyone',
            ]
            // Add more data here as needed
        ];
        DB::table('icebreakers')->insert($data);
        
    }
}
