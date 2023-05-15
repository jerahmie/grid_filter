pub mod sum_of_squares;
use pyo3::{prelude::*, types::PyList};
use sum_of_squares::sum_of_squares;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// Calculates the sum of squares of a python list of integers
#[pyfunction]
fn sum_of_squares_rs(a: &PyList) -> PyResult<usize> {
    let v: Vec<usize> = a.extract()?; 
    Ok(sum_of_squares(&v))
}

/// A Python module implemented in Rust.
#[pymodule]
fn grid_perimeter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(sum_of_squares_rs, m)?)?;
    Ok(())
}
