X(:,1) = [26,11,7,17,41,55,35,52,43,31,22,26,50,55,54,60,47,30,30,12,15,16,21,50,51,50,48,12,15,29,54,55,67,10,6];
X(:,2) = [13,28,43,64,46,34,16,26,26,76,53,29,40,50,10,15,66,60,50,17,14,19,48,30,42,15,21,38,56,39,38,57,41,70,25];

Dmax = 11.5;
n = rand(1, 5);

F = [];
F(1, 1) = 3 * Dmax * (1 + n(1));

for k = 2:5
   F(k, 1) = F(k - 1) * (1 + n(k)); 
end

randX = rand(35, 1); 

orderSum = sum(randX);

m = [];
for j = 1:35
    m(j, 1) = randX(j) / orderSum;
end

Q = zeros(5, 35); 
for i = 1:5
   for j = 1:35
       Q(i, j) = m(j) * F(i, 1);
   end
end

Qmax = 0;
for i = 1:5
   for j = 1:35
       if Q(i, j) > Qmax
           Qmax = Q(i, j);
       end
   end
end

if Qmax >= Dmax
   Dmax = Qmax + 0.1 * Qmax; 
end

figure;
scatter(X(:, 1), X(:, 2), 'o', 'filled', 'MarkerFaceColor', 'b', 'MarkerEdgeColor', 'k');
hold on;
scatter(40, 40, 'o', 'filled', 'MarkerFaceColor', 'r', 'MarkerEdgeColor', 'k');

for i = 1:length(X(:, 1))
    text(X(i, 1), X(i, 2) + 2, num2str(i + 7), 'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
end
