<?php

namespace App\Http\Controllers;

use Illuminate\View\View;

class TestController extends Controller
{
    /**
     * Retrieve the test for the given IDs.
     *
     * @param int $testId
     * @param int $commentId
     * @return View
     */
    public function show(int $testId, int $commentId): View
    {

        return view('test/show', [
            'testId' => $testId,
            'commentId' => $commentId
        ]);
    }
}
