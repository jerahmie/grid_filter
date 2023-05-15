use rayon::prelude::*;

pub fn sum_of_squares(input: &[usize]) -> usize {
    input.par_iter()
        .map(|&i| i * i)
        .sum()
}

