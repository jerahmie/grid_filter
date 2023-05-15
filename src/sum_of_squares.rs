//use rayon::prelude::*;

pub fn sum_of_squares(input: &[usize]) -> usize {
    input.iter()
        .map(|&i| i * i)
        .sum()
}

