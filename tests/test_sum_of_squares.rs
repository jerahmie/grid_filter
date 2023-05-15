use grid_filter::sum_of_squares::*;

//fn sum_of_squares(arr: &[i32]) -> i32 {
//    5
//}

#[cfg(test)]
    #[test]
    fn it_works() {
        let arr: Vec<i32> = (0..10).collect();
        //let result = sum_of_squares(arr).unwrap();
        let result = sum_of_squares(&arr);
        assert_eq!(result, 285);
    }
