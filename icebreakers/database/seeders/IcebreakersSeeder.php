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
                'statements' => 'If animals could talk, which species do you think would be the rudest?',
            ],
            [
                'id' => 2,
                'statements' => 'If you could only eat one color of food for the rest of your life, what color would it be?',
            ],
            [
                'id' => 3,
                'statements' => 'Chicken Rice, Nasi Lemak or Hokkien Mee. Choose one and tell us where is your go to place!',
            ],
            [
                'id' => 4,
                'statements' => 'Do the chicken dance',
            ],
            [
                'id' => 5,
                'statements' => 'When using a squat toilet, do you face the door or face the flush?',
            ],
            [
                'id' => 6,
                'statements' => 'If you were a professional wrestler, what would your entrance music be and what would your signature move be called?',
            ]
            // Add more data here as needed
        ];
        DB::table('icebreakers')->insert($data);
        
    }
}
