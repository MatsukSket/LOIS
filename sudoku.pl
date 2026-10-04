num(1).
num(2).
num(3).
num(4).


all_diff(A, B, C, D) :-
    num(A), num(B), num(C), num(D),
    A \= B, A \= C, A \= D, 
    B \= C, B \= D,
    C \= D.


sudoku(
    [A11, A12, A13, A14],
    [A21, A22, A23, A24],
    [A31, A32, A33, A34],
    [A41, A42, A43, A44]
) :-
    all_diff(A11, A12, A13, A14),
    all_diff(A21, A22, A23, A24),
    all_diff(A31, A32, A33, A34),
    all_diff(A41, A42, A43, A44),

    all_diff(A11, A21, A31, A41),
    all_diff(A12, A22, A32, A42),
    all_diff(A13, A23, A33, A43),
    all_diff(A14, A24, A34, A44),

    all_diff(A11, A12, A21, A22),
    all_diff(A13, A14, A23, A24),
    all_diff(A31, A32, A41, A42),
    all_diff(A33, A34, A43, A44).


solve(Matrix) :-
    (
        Matrix = [R1, R2, R3, R4],
        sudoku(R1, R2, R3, R4)
    ->
        print_matrix(Matrix)
    ;
        writeln('There is no solution.')
    ).


print_matrix([]).
print_matrix([Row|Rows]) :-
    writeln(Row),
    print_matrix(Rows).
