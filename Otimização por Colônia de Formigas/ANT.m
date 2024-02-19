% Aplicação do Ant Colony Optimization em Projetos de Circuitos Elétricos

tic
resp = [];
for super = 1:50
close all
clc
warning off

% NUMERO DE FORMIGAS EXISTENTES NO FORMIGUEIRO
NFORMIGAS = 100;

XFOB = []; 
XFORMIGAS = []; 
vic = 0;
candidatas = [];
FOBcand = [];
minFOBcand = [];
aux = 0;
XFOBcand = [];
XFORMIGAScand = [];
XMF1 = [];
XMF2 = [];
XMF3 = [];
XMF4 = [];
aux2 = 0;


LIMITES = 18; 

MF1 = zeros(1,LIMITES);
MF2 = zeros(1,LIMITES);
MF3 = zeros(1,LIMITES);
MF4 = zeros(1,LIMITES);

for i = 1:NFORMIGAS
    for j = 1:4
    n = round((rand*(LIMITES)));  
    
    if n == 0
        n = 1;
    end
    FORMIGAS(i,j) = n;             
    end
end

SOMA = [];
for k = 1:1:NFORMIGAS
SOMA(k) = sum(FORMIGAS(k,:));
end

SOMA = SOMA';

iter = 0;
conv = 0;
v2m = [];

while  iter <= 200
    
      iter = iter+1
                   
            for i=1:NFORMIGAS
                
               if FORMIGAS(i,1) == 0;  FORMIGAS(i,1) = 1; end
               if FORMIGAS(i,2) == 0;  FORMIGAS(i,2) = 1; end
               if FORMIGAS(i,3) == 0;  FORMIGAS(i,3) = 1; end
               if FORMIGAS(i,4) == 0;  FORMIGAS(i,4) = 1; end

                               
                R1 = FORMIGAS(i,1);
                R2 = FORMIGAS(i,2);
                R3 = FORMIGAS(i,3);
                R4 = FORMIGAS(i,4);
                
                v1 = (36 - 4.5*R2 - 1.5*R4)/(1+((R4+R2)/R1));
                v2 = 36 + (-R4/R1)*v1 - 1.5*R4;
                v2m = [v2m v2];
                
                cand = [R1 R2 R3 R4];
                if v2/R3 == 3
                    vic = 1;
                    aux = aux + 1;
                    pen = 10^3;
                    candidatas = [candidatas; FORMIGAS(i,:)];
                    FOBcand = [FOBcand R1+R2+R3+R4];
                    MINFOBcand = min(FOBcand);
                    poscand = find(FOBcand == MINFOBcand);
                    cand = candidatas(poscand(1),:);
                    if aux > 1 && FOBcand(aux) < FOBcand(aux-1)
                       pen = 0;
                    end
                    if aux > 1 && FOBcand(aux) > FOBcand(aux-1)
                       pen = 10^7;
                    end
                else
                    pen = 10^15;
                end

     
                FOB(i) = (R1 + R2 + R3 + R4);
              
                % DEPOSITO DE FEROMONIO NA MATRIZ
                MF1(R1) = MF1(R1) + (1/(FOB(i) + 0.00001  + pen));
                MF2(R2) = MF2(R2) + (1/(FOB(i) + 0.00001  + pen));
                MF3(R3) = MF3(R3) + (1/(FOB(i) + 0.00001  + pen));
                MF4(R4) = MF4(R4) + (1/(FOB(i) + 0.00001  + pen));
                          
            end
            
               XMF1 = [XMF1; MF1];
               XMF2 = [XMF2; MF2];
               XMF3 = [XMF3; MF3];
               XMF4 = [XMF4; MF4];

               MINFOB = min(FOB);
               posM = find(FOB==MINFOB);
               posM = posM(1);
               XFOB = [XFOB; MINFOB];
               XFORMIGAS = [XFORMIGAS; FORMIGAS(posM,:)];

              XFOBcand = [XFOBcand; min(FOBcand)];
              MINFOBcand = min(FOBcand);
              aux1 = find(FOBcand == MINFOBcand);
              
                   if vic == 1
                      aux2 = aux2 + 1;
                      XFORMIGAScand = [XFORMIGAScand; candidatas(aux1(1),:)];
                   end
                 
                  
             %######################################################################################### 
             % MONTAGEM DA ROLETA 
             %##########################################################################################
            
             % INCIALIZANDO DA ROLETA 
               cassino1 = [];  
               
             % SOMATORIO DA QUANTIDADE DE FEROMONIO
               TOTAL_FER1 = sum(sum(MF1));     
               TOTAL_FER2 = sum(sum(MF2)); 
               TOTAL_FER3 = sum(sum(MF3)); 
               TOTAL_FER4 = sum(sum(MF4)); 
                
             % PEDAÇO DA ROLETA REFERNTE A SOLUÇÃO
               fatia_coluna1 = ((MF1)/TOTAL_FER1)*100;
               fatia_coluna2 = ((MF2)/TOTAL_FER2)*100;
               fatia_coluna3 = ((MF3)/TOTAL_FER3)*100;
               fatia_coluna4 = ((MF4)/TOTAL_FER4)*100;
               
               
               fatia_coluna1 = ceil(fatia_coluna1); 
               fatia_coluna2 = ceil(fatia_coluna2);
               fatia_coluna3 = ceil(fatia_coluna3);
               fatia_coluna4 = ceil(fatia_coluna4);
               
             % DETERMINANDO DAS POSICOES COM RASTROS DE FEROMONIO
               pos_col1 = find(fatia_coluna1>0); 
               pos_col2 = find(fatia_coluna2>0);
               pos_col3 = find(fatia_coluna3>0);
               pos_col4 = find(fatia_coluna4>0);
 
              % DETERMINANDO DO NUMERO (ELEMENTOS)DE POSICAOO COM RASTROS DE FEROMONIO 
                [nl1,ncol1] = size(pos_col1); 
                [nl2,ncol2] = size(pos_col2);
                [nl3,ncol3] = size(pos_col3);
                [nl4,ncol4] = size(pos_col4);
               
              % MONTAGEM DA ROLETA
                cont=0;
                
              % GUARDA O PONTO DE TROCA DAS FATIAS (SOLUÇOES) DENTRO DA ROLETA  
                guarda1=0; guarda2=0; guarda3=0; guarda4=0;
                cassino_coluna1=[]; cassino_coluna2=[]; cassino_coluna3=[]; cassino_coluna4=[];

                
                for ii = 1:ncol1
                    while cont < fatia_coluna1(pos_col1(ii)) + guarda1
                         cont = cont+1;
                         cassino_coluna1(cont) = ii;
                    end
                    guarda1 = cont; 
                end
                
                cont = 0;
                for ii = 1:ncol2
                    while cont < fatia_coluna2(pos_col2(ii)) + guarda2
                         cont = cont+1;
                         cassino_coluna2(cont) = ii;
                    end
                    guarda2 = cont; 
                end
                
                cont = 0;
                for ii = 1:ncol3
                    while cont < fatia_coluna3(pos_col3(ii)) + guarda3
                         cont = cont+1;
                         cassino_coluna3(cont) = ii;
                    end
                    guarda3 = cont; 
                end
                
                cont = 0;
                for ii = 1:ncol4
                    while cont < fatia_coluna4(pos_col4(ii)) + guarda4
                         cont = cont+1;
                         cassino_coluna4(cont) = ii;
                    end
                    guarda4 = cont; 
                end
                                 
               [LLL1,CCC1] = size(cassino_coluna1); 
               [LLL2,CCC2] = size(cassino_coluna2);
               [LLL3,CCC3] = size(cassino_coluna3);
               [LLL4,CCC4] = size(cassino_coluna4);
                
              %###################################################################################### 
              % SORTEIO DAS SOLUÇÕES COM BASE NA ROLETA MONTADA
              %######################################################################################
               
              pos = 0;
              for it = 1:NFORMIGAS              
                  
                    DECISAO = rand*100; %
                    FORMIGAS(it,:) = 0;
                    
                    %FORMIGAS SEGUEM O RASTRO DE FEROMONIO (a roleta)
                    if (DECISAO <= 80) 
                        
                       % RODO A ROLETA
                       sorteio1 = round(rand(1)*(CCC1-1))+1; 
                       sorteio2 = round(rand(1)*(CCC2-1))+1;
                       sorteio3 = round(rand(1)*(CCC3-1))+1;
                       sorteio4 = round(rand(1)*(CCC4-1))+1;
                       
                       
                       % POSICAO OBTIDA PELO CASSINO
                       posicao_col1 = cassino_coluna1(sorteio1); 
                       posicao_col2 = cassino_coluna2(sorteio2);
                       posicao_col3 = cassino_coluna3(sorteio3);
                       posicao_col4 = cassino_coluna4(sorteio4);
                       
                       % VALOR DA RAIZ
                       FORMIGAS(it,1) = pos_col1(posicao_col1);
                       FORMIGAS(it,2) = pos_col2(posicao_col2);
                       FORMIGAS(it,3) = pos_col3(posicao_col3);
                       FORMIGAS(it,4) = pos_col4(posicao_col4);                                                         
                    end
                    
                   if (DECISAO > 30 && DECISAO <= 80)
                       FORMIGAS(it,1) = ceil(rand*cand(1));
                       FORMIGAS(it,2) = ceil(rand*cand(2));
                       FORMIGAS(it,3) = ceil(rand*cand(3));
                       FORMIGAS(it,4) = ceil(rand*cand(4));                       
                   end
                   
                   if (DECISAO >= 81)
                       n = round((rand*(LIMITES)));
                       if n == 0
                           n = 1;
                       end
                       FORMIGAS(it,1) = n;
                       
                       n = round((rand*(LIMITES)));
                       if n == 0
                           n = 1;
                       end
                       FORMIGAS(it,2) = n;
                       
                       n = round((rand*(LIMITES)));
                       if n == 0
                           n = 1;
                       end
                       FORMIGAS(it,3) = n;
                       
                       n = round((rand*(LIMITES)));
                       if n == 0
                           n = 1;
                       end
                       FORMIGAS(it,4) = n;                                             
                   end
               end
               
              %######################################################################################
              %  EVAPORACAO DA MATRIZ DE FEROMONIO
              %##########################################################################%############
             
              % TAXA DE EVAPORACAO - 20% 
             
              if iter <= 150
                  sigma1 = 0.8; sigma2 = 0.8; sigma3 = 0.8; sigma4 = 0.8;
              else
                  sigma1 = 0.25;
                  sigma2 = 0.25;
                  sigma3 = 0.25;
                  sigma4 = 0.25; 
              end
                         
              % EVAPORAÇAO NA MATRIZ DE FEROMONIO
              MF1 = (1-sigma1).*MF1;
              MF2 = (1-sigma2).*MF2; 
              MF3 = (1-sigma3).*MF3; 
              MF4 = (1-sigma4).*MF4; 
              
              v2m = [];
              vic = 0;        
              
end
XFORMIGAScand

if size(XFORMIGAScand) ~= 0
resp = [resp; XFORMIGAScand(end,:)];
end
end

certo = 0;
for k = 1:size(resp)
    if resp(k,1) == 2 && resp(k,2) == 1 && resp(k,3) == 6 && resp(k,4) == 3
        certo = certo + 1;
    end
end

tx = (certo/super)*100;

fprintf('Taxa de acerto: %.2f\n',tx)

toc

% Adicionar gráfico

% Vetores de percentuais
percentuais = [tx, tx, tx, tx];

% Criando o gráfico de barras
figure;
bar(percentuais);
xlabel('Resistores');
ylabel('Percentual de escolha');
title('Acertividade na escolha dos resistores');

% Ajustando o layout
grid on;