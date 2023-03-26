use smallvec::SmallVec;
// most strings are short, so we can use a fixed-size array
const VEC_SIZE: usize = 32;

pub type FastVec<T> = SmallVec<[T; VEC_SIZE]>;
