  %1 = alloca i32, align 4
  %a = alloca [10 x i32], align 16
  %b = alloca [10 x i32], align 16
  %c = alloca [10 x i32], align 16
  %i = alloca i32, align 4
  %i1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 0, i32* %i, align 4
  %4 = load i32, i32* %i, align 4
  %5 = icmp slt i32 %4, 10
  %8 = load i32, i32* %i, align 4
  %9 = load i32, i32* %i, align 4
  %10 = sext i32 %9 to i64
  %11 = getelementptr inbounds [10 x i32], [10 x i32]* %a, i64 0, i64 %10
  store i32 %8, i32* %11, align 4
  %21 = getelementptr inbounds [10 x i32], [10 x i32]* %a, i32 0, i32 0
  %22 = getelementptr inbounds [10 x i32], [10 x i32]* %b, i32 0, i32 0
  %23 = getelementptr inbounds [10 x i32], [10 x i32]* %c, i32 0, i32 0
  call void @add(i32* %21, i32* %22, i32* %23)
