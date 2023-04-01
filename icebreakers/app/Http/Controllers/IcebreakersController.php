<?php

namespace App\Http\Controllers;

use app\Models\Icebreakers;
use Illuminate\Support\Facades\DB;
use Illuminate\View\View;
use Illuminate\Http\Request;

class IcebreakersController extends Controller
{
    //INSERT INTO `icebreakers` (`id`, `statement`) VALUES ('1', 'What is your favourite food?');

    public function __invoke()
    {
        $random_number = rand(1,6);
        $all = DB::table('icebreakers')
                -> where('id','=',$random_number)      
                ->get();
     
        return $all[0];
        

    }
}
