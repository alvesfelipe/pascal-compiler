program Test3; {programa exemplo 2}
var
   NUMERO, m : integer;
   final, teste : integer;
   bool : boolean;
   NUMB : real;

procedure findMin(x, y, z: integer; war: integer); 
var
    m : integer;
begin
   if x < y then
      m := x;
   else
      m := y;
   
   if z < m then
      m := z;
end;

begin  {tente gerar um erro usando um caracter nao permitido.. tipo $}
   NUMERO := 3 * 5 + 10 - 9;

   if (NUMERO >= 20) and (NUMERO <=90) then begin
      NUMERO := 10;
      final := NUMERO + 1;
   end;

    bool := NUMERO > final;
end.
